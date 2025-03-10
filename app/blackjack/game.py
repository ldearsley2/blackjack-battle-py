import requests

from app.blackjack.card_calculator import CardCalculator
from app.blackjack.card_manager import CardManager
from app.blackjack.player import Player
from app.services.game_service import GameService


class BlackJackGame:
    """
    BlackJackGame is responsible for maintaining game state.
    """

    def __init__(
        self,
        card_manager: CardManager,
        card_calc: CardCalculator,
    ):
        self.card_manager: CardManager = card_manager
        self.card_calc: CardCalculator = card_calc
        self.dealer_cards: list[str] = []
        self.dealer_stop: int = 17
        self.max_hand: int = 21
        self.players: list[Player] = []
        self.finished_players: list[Player] = []

    def add_players(self, game_service: GameService):
        """
        Populate the game's players with game_service's connected players
        """
        for player_id, url in game_service.connected_players.items():
            self.players.append(Player(player_id=str(player_id), url=url, points=10))

    def dealer_add_to_hand(self):
        """
        Add a card to the dealers hand
        """
        self.dealer_cards.append(self.card_manager.play_card())

    def deal_cards(self):
        """
        Starting point for a round, deal one card to dealer, two to each player.
        """
        self.dealer_add_to_hand()
        for p in self.players:
            for i in range(2):
                p.add_to_hand(self.card_manager.play_card())

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
        }
        return hand_json

    def play_hand(self, player: Player):
        player.play_state = "Playing"

        while player.play_state == "Playing":
            response = requests.post(
                url=f"{player.url}/turn", json=self.create_hand_json(player)
            )
            action = response.json()["action"]

            if action == "Hit":
                player.hand.append(self.card_manager.play_card())
                if self.card_calc.has_busted(
                    self.card_calc.get_hand_value(player.hand)
                ):
                    player.play_state = "Busted"

            if action == "Stand":
                player.play_state = "Stand"
                break

    def bust_players(self, players: list[Player], dealer_score: int):
        """
        Find and bust players with score less than the dealers
        """
        for p in players:
            if p.play_state == "Busted":
                continue
            player_score = self.card_calc.get_hand_value(p.hand)
            if dealer_score >= player_score:
                p.play_state = "Busted"

    def adjust_points(self):
        """
        Adjust each player's points based on their play_state
        """
        for p in self.players:
            if p.play_state == "playing":
                p.add_points(1)
            else:
                p.remove_points(1)
                if p.points == 0:
                    self.finished_players.append(p)
                    self.players.remove(p)

    def round_cleanup(self):
        """
        Reset object fields for the next round of blackjack
        """
        for p in self.players:
            p.play_state = ""
            p.clear_hand()
        self.dealer_cards = []
        self.card_manager.shuffle_check()

    def log_current_state(self):
        print(f"| Player_id | Hand | Status |")
        for p in self.players:
            print(f"| {p.player_id } | {p.hand} | {p.play_state} |")


    def play_round(self):
        # Deal cards to all players and dealer
        self.deal_cards()

        self.log_current_state()

        # Each player plays their hand
        for player in self.players:
            self.play_hand(player)

        self.log_current_state()

        # Dealer plays hand
        self.dealer_add_to_hand()
        dealer_score = self.card_calc.get_hand_value(self.dealer_cards)

        # Dealer draws one card and is over dealer stop limit
        if dealer_score >= self.dealer_stop:
            self.bust_players(self.players, dealer_score)

        # Dealer continues to draw cards until at or over dealer stop limit
        while dealer_score < self.dealer_stop:
            self.dealer_add_to_hand()
            dealer_score = self.card_calc.get_hand_value(self.dealer_cards)

        # If dealer busts, award remaining players with points
        if dealer_score > self.max_hand:
            self.adjust_points()
        else:
            # Bust players with less score than dealer
            self.bust_players(self.players, dealer_score)
            # Award and remove points
            self.adjust_points()

        self.round_cleanup()
