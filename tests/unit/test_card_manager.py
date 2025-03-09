import unittest

from app.blackjack.card_manager import CardManager


class TestCardManager(unittest.TestCase):
    def test_cm_init(self):
        card_manager = CardManager(decks=1, shuffle_limit=20)

        expected = [
            "2H",
            "3H",
            "4H",
            "5H",
            "6H",
            "7H",
            "8H",
            "9H",
            "10H",
            "JH",
            "QH",
            "KH",
            "AH",
            "2D",
            "3D",
            "4D",
            "5D",
            "6D",
            "7D",
            "8D",
            "9D",
            "10D",
            "JD",
            "QD",
            "KD",
            "AD",
            "2C",
            "3C",
            "4C",
            "5C",
            "6C",
            "7C",
            "8C",
            "9C",
            "10C",
            "JC",
            "QC",
            "KC",
            "AC",
            "2S",
            "3S",
            "4S",
            "5S",
            "6S",
            "7S",
            "8S",
            "9S",
            "10S",
            "JS",
            "QS",
            "KS",
            "AS",
        ]

        self.assertEqual(1, card_manager.decks)
        self.assertEqual(expected, card_manager.cards)

    def test_cm_populate_cards(self):
        card_manager = CardManager(decks=1, shuffle_limit=20)

        expected = [
            "2H",
            "3H",
            "4H",
            "5H",
            "6H",
            "7H",
            "8H",
            "9H",
            "10H",
            "JH",
            "QH",
            "KH",
            "AH",
            "2D",
            "3D",
            "4D",
            "5D",
            "6D",
            "7D",
            "8D",
            "9D",
            "10D",
            "JD",
            "QD",
            "KD",
            "AD",
            "2C",
            "3C",
            "4C",
            "5C",
            "6C",
            "7C",
            "8C",
            "9C",
            "10C",
            "JC",
            "QC",
            "KC",
            "AC",
            "2S",
            "3S",
            "4S",
            "5S",
            "6S",
            "7S",
            "8S",
            "9S",
            "10S",
            "JS",
            "QS",
            "KS",
            "AS",
        ]

        self.assertEqual(expected, card_manager.cards)

    def test_populate_two_decks(self):
        card_manager = CardManager(decks=2, shuffle_limit=20)

        expected = [
            "2H",
            "3H",
            "4H",
            "5H",
            "6H",
            "7H",
            "8H",
            "9H",
            "10H",
            "JH",
            "QH",
            "KH",
            "AH",
            "2D",
            "3D",
            "4D",
            "5D",
            "6D",
            "7D",
            "8D",
            "9D",
            "10D",
            "JD",
            "QD",
            "KD",
            "AD",
            "2C",
            "3C",
            "4C",
            "5C",
            "6C",
            "7C",
            "8C",
            "9C",
            "10C",
            "JC",
            "QC",
            "KC",
            "AC",
            "2S",
            "3S",
            "4S",
            "5S",
            "6S",
            "7S",
            "8S",
            "9S",
            "10S",
            "JS",
            "QS",
            "KS",
            "AS",
            "2H",
            "3H",
            "4H",
            "5H",
            "6H",
            "7H",
            "8H",
            "9H",
            "10H",
            "JH",
            "QH",
            "KH",
            "AH",
            "2D",
            "3D",
            "4D",
            "5D",
            "6D",
            "7D",
            "8D",
            "9D",
            "10D",
            "JD",
            "QD",
            "KD",
            "AD",
            "2C",
            "3C",
            "4C",
            "5C",
            "6C",
            "7C",
            "8C",
            "9C",
            "10C",
            "JC",
            "QC",
            "KC",
            "AC",
            "2S",
            "3S",
            "4S",
            "5S",
            "6S",
            "7S",
            "8S",
            "9S",
            "10S",
            "JS",
            "QS",
            "KS",
            "AS",
        ]

        self.assertEqual(expected, card_manager.cards)

    def test_play_card(self):
        card_manager = CardManager(decks=1, shuffle_limit=20)
        card_manager.play_card()

        self.assertEqual(51, len(card_manager.cards))
        self.assertEqual(1, len(card_manager.played_cards))

    def test_play_card_empty_list(self):
        card_manager = CardManager(decks=0, shuffle_limit=20)

        self.assertEqual(None, card_manager.play_card())

    def test_reset_cards(self):
        card_manager = CardManager(decks=1, shuffle_limit=20)

        card_manager.play_card()
        card_manager.play_card()

        self.assertEqual(50, len(card_manager.cards))
        self.assertEqual(2, len(card_manager.played_cards))

        card_manager.reset_cards()

        self.assertEqual(52, len(card_manager.cards))
        self.assertEqual(0, len(card_manager.played_cards))
