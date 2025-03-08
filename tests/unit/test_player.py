import unittest

from app.blackjack.player import Player


class TestPlayer(unittest.TestCase):
    def test_add_points(self):
        player = Player("1", "https://www.foo.com/", 10)
        player.add_points(10)
        expected = 20
        self.assertEqual(expected, player.points)

    def test_remove_points(self):
        player = Player("1", "https://www.foo.com/", 10)
        player.remove_points(5)
        expected = 5
        self.assertEqual(expected, player.points)

    def test_remove_over_current(self):
        player = Player("1", "https://www.foo.com/", 10)
        player.remove_points(20)
        expected = 0
        self.assertEqual(expected, player.points)
