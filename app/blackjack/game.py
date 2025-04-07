import asyncio

import requests

from app.blackjack.card_calculator import CardCalculator
from app.blackjack.card_manager import CardManager
from app.blackjack.dealer import Dealer
from app.blackjack.player import Player, PlayStates
from app.blackjack.player_manager import PlayerManager
from app.services.state_service import StateService
from app.sockets import broadcast_update


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
        dealer_stop: int,
    ):
        self.card_manager: CardManager = CardManager(
            decks=decks, shuffle_limit=shuffle_limit
        )
        self.card_calc: CardCalculator = CardCalculator(max_hand=max_hand)
        self.state_service = state_service
        self.dealer: Dealer = Dealer(stop_limit=dealer_stop)
        self.max_hand: int = max_hand
        self.player_manager: PlayerManager = PlayerManager()
        self.turn_wait: float = 0.5
        self.round_wait: float = 2.0

    def update_state_service(self):
        """
        Get current game state and update the state service
        """
        current_state = {"players": [], "dealer_hand": self.dealer.get_cards()}
        for player in self.player_manager.players:
            player_state = {
                "nickname": player.player_nickname,
                "points": player.points,
                "bet_amount": player.get_bet_amount(),
                "hand": player.hand,
                "play_status": player.get_play_state(),
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
            "dealer_stop": str(self.dealer.get_stop_limit()),
            "dealer_hand": self.dealer.get_cards(),
            "current_hand": player.hand,
            "played_cards": self.card_manager.played_cards,
            "deck_amount": str(self.card_manager.decks),
        }
        return hand_json

    async def get_player_bet(self, player: Player):
        """
        Get a players bet, disqualify if bet is too large.
        """
        bet_json = {
            "player_id": player.player_id,
            "current_points": player.get_points(),
        }
        try:
            response = requests.post(url=f"{player.url}/bet", json=bet_json, timeout=10)
            bet_amount = response.json()["bet_amount"]
            if bet_amount > player.get_points():
                player.set_play_state(PlayStates.DISQUALIFIED)
                self.player_manager.finished_players.append(player)
                self.player_manager.players.remove(player)
            else:
                player.set_bet_amount(bet_amount)

        except Exception as e:
            print(e)

    async def get_player_bets(self):
        """
        Get all players bets.
        """
        for player in self.player_manager.players:
            await self.get_player_bet(player)

    async def deal_cards(self):
        """
        Starting point for a round, deal one card to dealer, two to each player.
        """
        self.dealer.add_to_cards(self.card_manager.play_card())
        for player in self.player_manager.players:
            player.play_state = PlayStates.PLAYING
            for i in range(2):
                player.add_to_hand(self.card_manager.play_card())

                self.update_state_service()
                await broadcast_update(self.state_service.get_game_state())
                await asyncio.sleep(self.turn_wait)

            player.hand_value = self.card_calc.get_hand_value(player.hand)

    async def play_hand(self, player: Player):
        while player.get_play_state() == PlayStates.PLAYING.value:
            try:
                response = requests.post(
                    url=f"{player.url}/turn",
                    json=self.create_hand_json(player),
                    timeout=10,
                )
                action = response.json()["action"]

                if action == "Hit":
                    player.hand.append(self.card_manager.play_card())
                    player.hand_value = self.card_calc.get_hand_value(player.hand)
                    if player.hand_value > self.max_hand:
                        player.set_play_state(PlayStates.BUSTED)
                if action == "Stand":
                    player.set_play_state(PlayStates.STAND)
                    break

                self.update_state_service()
                await broadcast_update(self.state_service.get_game_state())
                await asyncio.sleep(self.turn_wait)

            except requests.Timeout:
                print(f"{player.player_id} did not take an action within timeout")
                player.set_play_state(PlayStates.TIMEOUT)
                self.player_manager.finished_players.append(player)
                self.player_manager.players.remove(player)
            except requests.ConnectionError:
                print(f"{player.player_id} lost connection")
                player.set_play_state(PlayStates.CONNECTION_LOSS)
                self.player_manager.finished_players.append(player)
                self.player_manager.players.remove(player)

    def round_cleanup(self):
        """
        Reset object fields for the next round of blackjack
        """
        for p in self.player_manager.players:
            p.set_play_state(PlayStates.WAITING)
            p.reset_bet_amount()
            p.clear_hand()
        self.dealer.remove_cards()
        self.card_manager.shuffle_check()

    async def play_round(self):
        """
        Play a full round of blackjack
        """
        # Get bet amounts
        await self.get_player_bets()

        # Deal cards to all players and dealer
        await self.deal_cards()

        # Each player plays their hand
        for player in self.player_manager.players:
            await self.play_hand(player)

        # Dealer plays hand
        self.dealer.add_to_cards(self.card_manager.play_card())
        dealer_score = self.card_calc.get_hand_value(self.dealer.get_cards())
        self.update_state_service()
        await broadcast_update(self.state_service.get_game_state())
        await asyncio.sleep(self.turn_wait)

        # Dealer draws one card and is over dealer stop limit
        if dealer_score >= self.dealer.get_stop_limit():
            self.player_manager.set_players_status(dealer_score)

        # Dealer continues to draw cards until at or over dealer stop limit
        while dealer_score < self.dealer.get_stop_limit():
            self.dealer.add_to_cards(self.card_manager.play_card())
            dealer_score = self.card_calc.get_hand_value(self.dealer.get_cards())
            self.update_state_service()
            await broadcast_update(self.state_service.get_game_state())
            await asyncio.sleep(self.turn_wait)

        # If dealer busts, award remaining players with points
        if dealer_score > self.max_hand:
            self.player_manager.adjust_player_points()
        else:
            # Bust players with less score than dealer
            self.player_manager.set_players_status(dealer_score)
            # Award and remove points
            self.player_manager.adjust_player_points()

        await asyncio.sleep(self.round_wait)
        self.round_cleanup()
