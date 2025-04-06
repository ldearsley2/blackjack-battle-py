import unittest

from app.services.game_service import GameService, GSPlayer


class TestGameServiceAdd(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService()


class TestGameServiceRemove(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService()
        self.game_service.connected_players = {
            "1": GSPlayer("foo", "https://www.bar.com/"),
            "2": GSPlayer("bar", "https://www.bar.com/"),
            "3": GSPlayer("baz", "https://www.baz.com/"),
            "4": GSPlayer("buz", "https://www.buz.com/"),
        }

    def test_remove_one_player(self):
        self.game_service.remove_player("2")

        expected = {
            "1": GSPlayer("foo", "https://www.bar.com/"),
            "3": GSPlayer("baz", "https://www.baz.com/"),
            "4": GSPlayer("buz", "https://www.buz.com/"),
        }

        self.assertEqual(expected, self.game_service.connected_players)

    def test_remove_two_player(self):
        self.game_service.remove_player("2")
        self.game_service.remove_player("4")

        expected = {
            "1": GSPlayer("foo", "https://www.bar.com/"),
            "3": GSPlayer("baz", "https://www.baz.com/"),
        }

        self.assertEqual(expected, self.game_service.connected_players)

    def test_remove_unknown_player(self):
        with self.assertRaises(KeyError):
            self.game_service.remove_player("5")

    def test_can_connect(self):
        self.game_service.connected_players = {
            "1": GSPlayer("foo", "https://www.foo.com/"),
            "2": GSPlayer("baz", "https://www.baz.com/"),
        }

        self.assertFalse(self.game_service.can_connect("https://www.foo.com/"))

    def test_can_connect_true(self):
        self.game_service.connected_players = {
            "1": GSPlayer("foo", "https://www.foo.com/")
        }

        self.assertTrue(self.game_service.can_connect("https://www.bar.com/"))
