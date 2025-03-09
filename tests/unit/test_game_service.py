import unittest

from app.services.game_service import GameService


class TestGameServiceAdd(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService()


class TestGameServiceRemove(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService()
        self.game_service.connected_players = {
            "1": "https://www.foo.com/",
            "2": "https://www.bar.com/",
            "3": "https://www.baz.com/",
            "4": "https://www.buz.com/",
        }

    def test_remove_one_player(self):
        self.game_service.remove_player("2")

        expected = {
            "1": "https://www.foo.com/",
            "3": "https://www.baz.com/",
            "4": "https://www.buz.com/",
        }

        self.assertEqual(expected, self.game_service.connected_players)

    def test_remove_two_player(self):
        self.game_service.remove_player("2")
        self.game_service.remove_player("4")

        expected = {
            "1": "https://www.foo.com/",
            "3": "https://www.baz.com/",
        }

        self.assertEqual(expected, self.game_service.connected_players)

    def test_remove_unknown_player(self):
        with self.assertRaises(KeyError):
            self.game_service.remove_player("5")
