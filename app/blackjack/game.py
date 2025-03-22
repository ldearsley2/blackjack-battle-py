import asyncio

import requests
from starlette.websockets import WebSocket

from app.blackjack.card_calculator import CardCalculator
from app.blackjack.card_manager import CardManager
from app.blackjack.player import Player
from app.dependencies import get_state_service
from app.services.game_service import GSPlayer
from app.services.state_service import StateService
from app.sockets import send_turn


class BlackJackGame:
    """
    BlackJackGame is responsible for maintaining game state.
    """

    def __init__(
        self,
        state_service: StateService,
        decks: int,
        shuffle_limit: int,
        max_hand: int,
    ):
        self.card_manager: CardManager = CardManager(decks=decks, shuffle_limit=shuffle_limit)
        self.card_calc: CardCalculator = CardCalculator(max_hand=max_hand)
        self.state_service = state_service
        self.dealer_cards: list[str] = []
        self.dealer_stop: int = 17
        self.max_hand: int = 21
        self.players: list[Player] = []
        self.finished_players: list[Player] = []

    def update_state_service(self):
        """
        Get current game state and update the state service
        """
        current_state = {"players": [], "dealer_hand": self.dealer_cards}
        for p in self.players:
            player_state = {
                "nickname": p.player_nickname,
                "points": p.points,
                "hand": p.hand,
                "play_status": p.play_state,
            }
            current_state["players"].append(player_state)

        self.state_service.set_game_state(current_state)

    def create_hand_json(self, player: Player):
        """
        Generate a hand json, contains all data needed by blackjack players to make a decision
        """
        hand_json = {
            "player_id": player.player_id,
            "player_max_hand": str(self.max_hand),
            "dealer_stop": str(self.dealer_stop),
            "dealer_hand": self.dealer_cards,
            "current_hand": player.hand,
            "played_cards": self.card_manager.played_cards,
            "deck_amount": str(self.card_manager.decks)
        }
        return hand_json

    def add_player(self, player_id: str, player_nickname: str, player_socket: WebSocket):
        self.players.append(Player(player_id, player_nickname, websocket=player_socket, points=10))
        print("Blackjack game added player")

    def dealer_add_to_hand(self):
        """
        Add a card to the dealers hand
        """
        self.dealer_cards.append(self.card_manager.play_card())

    async def deal_cards(self):
        """
        Starting point for a round, deal one card to dealer, two to each player.
        """
        self.dealer_add_to_hand()
        for p in self.players:
            p.play_state = "Playing"
            for i in range(2):
                p.add_to_hand(self.card_manager.play_card())

                self.update_state_service()
                await asyncio.sleep(0.4)

            p.hand_value = self.card_calc.get_hand_value(p.hand)

    async def play_hand(self, player: Player):
        while player.play_state == "Playing":

            await send_turn(player_id=player.player_id, turn_data=self.create_hand_json(player))
            action = response.get("action")

            if action == "Hit":
                player.hand.append(self.card_manager.play_card())
                player.hand_value = self.card_calc.get_hand_value(player.hand)
                if player.hand_value > self.max_hand:
                    player.player_state = "Busted"

            if action == "Stand":
                player.play_state = "Stand"
                break

            self.update_state_service()
            await asyncio.sleep(0.4)

    def set_players_status(self, players: list[Player], dealer_score: int):
        """
        Find and bust players with score less than the dealers, set status to draw if score is the same
        """
        for p in players:
            if p.play_state == "Busted":
                continue
            if dealer_score == p.hand_value:
                p.play_state = "Drew"
            if dealer_score > p.hand_value:
                p.play_state = "Busted"

    def adjust_points(self):
        """
        Adjust each player's points based on their play_state
        """
        for p in self.players:
            if p.play_state == "Drew":
                continue
            if not p.play_state == "Busted":
                p.add_points(1)
                p.play_state = "Win"
                self.log_round_end(p)
            else:
                p.remove_points(1)
                p.play_state = "Loss"
                self.log_round_end(p)
                if p.points == 0:
                    self.finished_players.append(p)
                    self.players.remove(p)

    def round_cleanup(self):
        """
        Reset object fields for the next round of blackjack
        """
        for p in self.players:
            p.play_state = "Waiting"
            p.clear_hand()
        self.dealer_cards = []
        self.card_manager.shuffle_check()

    def log_current_state(self):
        print("| Player_id | Hand | Status | Points |")
        for p in self.players:
            print(f"| {p.player_id} | {p.hand} | {p.play_state} | {p.points} |")

    def log_round_end(self, player: Player):
        print("| Player_id | Hand | Status | Points |")
        print(
            f"| {player.player_id} | {player.hand} | {player.play_state} | {player.points} |"
        )

    async def play_round(self):
        # Deal cards to all players and dealer
        await self.deal_cards()
        self.update_state_service()

        # Each player plays their hand
        for player in self.players:
            await self.play_hand(player)
            self.update_state_service()

        # Dealer plays hand
        self.dealer_add_to_hand()
        dealer_score = self.card_calc.get_hand_value(self.dealer_cards)
        self.update_state_service()

        # Dealer draws one card and is over dealer stop limit
        if dealer_score >= self.dealer_stop:
            self.set_players_status(self.players, dealer_score)

        # Dealer continues to draw cards until at or over dealer stop limit
        while dealer_score < self.dealer_stop:
            self.dealer_add_to_hand()
            dealer_score = self.card_calc.get_hand_value(self.dealer_cards)
            self.update_state_service()
            await asyncio.sleep(0.4)

        # If dealer busts, award remaining players with points
        if dealer_score > self.max_hand:
            self.adjust_points()
        else:
            # Bust players with less score than dealer
            self.set_players_status(self.players, dealer_score)
            # Award and remove points
            self.adjust_points()

        self.round_cleanup()
