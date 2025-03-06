import unittest

from app.blackjack.card_manager import CardManager
from app.blackjack.game import BlackJackGame
from app.services.game_service import GameService


class TestBlackjackAddPlayer(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService()
        self.game_service.add_player("https://www.foo.com")
        self.game_service.add_player("https://www.bar.com")

        self.card_manager = CardManager(decks=1)

        self.blackjack_game = BlackJackGame(self.card_manager, self.game_service)

    def test_add_players(self):
        self.blackjack_game.add_players()

        self.assertEqual(2, len(self.blackjack_game.players))