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
        game_service: GameService,
    ):
        self.card_manager: CardManager = card_manager
        self.card_calc: CardCalculator = card_calc
        self.dealer_cards: list[str] = []
        self.dealer_stop: int = 17
        self.max_hand: int = 21
        self.players: list[Player] = []
        self.game_service: GameService = game_service

    def add_players(self):
        """
        Populate the game's players with those within the attached game manager
        """
        for player_id, url in self.game_service.connected_players.items():
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

        def bust_check():
            if self.card_calc.contains_ace(player.hand):
                hand_score = self.card_calc.get_hand_value_with_ace(player.hand)
            else:
                hand_score = self.card_calc.get_hand_value_no_ace(player.hand)

            if self.card_calc.has_busted(hand_score):
                player.play_state = "Busted"

        while player.play_state == "Playing":
            response = requests.post(
                url=f"{player.url}/turn", json=self.create_hand_json(player)
            )
            action = response.json()["action"]

            if action == "Hit":
                player.hand.append(self.card_manager.play_card())
                bust_check()

            if action == "Stand":
                player.play_state = "Stand"
                break

    def play_round(self):
        # TODO Refactor

        # Deal cards to all players and dealer
        self.deal_cards()

        # Each player plays their hand
        for player in self.players:
            self.play_hand(player)

        # Dealer plays hand
        self.dealer_cards.append(self.card_manager.play_card())
        dealer_score = self.card_calc.get_hand_value(self.dealer_cards)

        # Dealer draws one card and is over dealer stop limit
        if dealer_score >= self.dealer_stop:
            for player in self.players:
                if player.play_state == "Busted":
                    continue
                player_score = self.card_calc.get_hand_value(player.hand)
                if dealer_score >= player_score:
                    player.play_state = "Busted"

        # Dealer continues to draw cards until at or over dealer stop limit
        while dealer_score < self.dealer_stop:
            self.dealer_cards.append(self.card_manager.play_card())
            dealer_score = self.card_calc.get_hand_value(self.dealer_cards)

            # If dealer busts, award remaining players with points
            if dealer_score > self.max_hand:
                for p in self.players:
                    if p.play_state == "Busted":
                        continue
                    p.points += 1

        # Final check to see if dealer has beat any remaining player
        for player in self.players:
            if player.play_state == "Busted":
                continue
            player_score = self.card_calc.get_hand_value(player.hand)
            if dealer_score >= player_score:
                player.play_state = "Busted"

        # Award remaining players with points
        for player in self.players:
            if player.play_state == "Busted":
                continue
            player.points += 1
