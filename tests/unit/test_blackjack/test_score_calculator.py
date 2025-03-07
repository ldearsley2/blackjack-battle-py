import unittest

from app.blackjack.score_calculator import CardCalculator


class TestScoreCalculator(unittest.TestCase):
    def setUp(self):
        self.card_calc = CardCalculator(max_hand=21)

    def test_get_card_value(self):
        card = "2H"
        expected = [2]
        actual = self.card_calc.get_card_value(card)

        self.assertEqual(expected, actual)

    def test_get_hand_value(self):
        hand = ["2H", "10C"]
        expected = 12
        actual = self.card_calc.get_hand_value_no_ace(hand)

        self.assertEqual(expected, actual)

    def test_hand_exceeds_max(self):
        hand = ["10H", "10C", "JC"]
        expected = -1
        hand_value = self.card_calc.get_hand_value_no_ace(hand)
        actual = self.card_calc.bust_check(hand_value)
        self.assertEqual(expected, actual)

    def test_ace_greater_than_max(self):
        hand = ["10H", "2C", "AC"]
        expected = 13
        actual = self.card_calc.get_hand_value_with_ace(hand)
        self.assertEqual(expected, actual)

    def test_two_ace(self):
        hand = ["AC", "AS"]
        expected = 12
        actual = self.card_calc.get_hand_value_with_ace(hand)
        self.assertEqual(expected, actual)

    def test_two_ace_greater_than_max(self):
        hand = ["AC", "5H", "AS"]
        expected = 17
        actual = self.card_calc.get_hand_value_with_ace(hand)
        self.assertEqual(expected, actual)