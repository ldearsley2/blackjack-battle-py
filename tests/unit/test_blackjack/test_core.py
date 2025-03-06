import unittest

from app.blackjack.card_manager import CardManager
from app.blackjack.game import BlackJackGame
from app.blackjack.player import Player
from app.services.game_service import GameService


class TestBlackjackCore(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService()
        self.game_service.add_player("https://www.foo.com")

        self.card_manager = CardManager(decks=1)

        self.blackjack_game = BlackJackGame(self.card_manager, self.game_service)

    def test_add_player(self):
        self.blackjack_game.add_players()

        self.assertEqual(1, len(self.blackjack_game.players))

    def test_players_setup(self):
        self.game_service.add_player("https://www.bar.com")

        self.blackjack_game.add_players()

        for p in self.blackjack_game.players:
            self.assertIsInstance(p, Player)
            self.assertEqual(10, p.points)

    def test_dealer_add_to_hand(self):
        self.assertEqual(0, len(self.blackjack_game.dealer_cards))

        self.blackjack_game.dealer_add_to_hand()

        self.assertEqual(1, len(self.blackjack_game.dealer_cards))

    def test_deal_cards(self):
        self.blackjack_game.add_players()
        self.blackjack_game.deal_cards()

        self.assertEqual(1, len(self.blackjack_game.dealer_cards))
        for p in self.blackjack_game.players:
            self.assertEqual(2, len(p.hand))
        self.assertEqual(49, len(self.card_manager.cards))
        self.assertEqual(3, len(self.card_manager.played_cards))

    def test_deal_cards_two_player(self):
        self.game_service.add_player("https://www.bar.com")
        self.blackjack_game.add_players()
        self.blackjack_game.deal_cards()

        self.assertEqual(1, len(self.blackjack_game.dealer_cards))
        for p in self.blackjack_game.players:
            self.assertEqual(2, len(p.hand))
        self.assertEqual(47, len(self.card_manager.cards))
        self.assertEqual(5, len(self.card_manager.played_cards))