import random
from app.blackjack.deck import DECK


class CardManager:
    def __init__(self, decks: int, shuffle_limit: int):
        """
        Maintains deck of cards
        :param decks:
        """
        self.cards: list = []
        self.played_cards: list = []
        self.decks: int = decks
        self.shuffle_limit = shuffle_limit
        self.populate_cards()

    def populate_cards(self) -> None:
        """
        Populate CardManager's cards with 52 times decks cards
        :return:
        """
        for i in range(self.decks):
            self.cards.extend(DECK)

    def play_card(self) -> str | None:
        """
        Select random card, add to played_cards and remove from cards. Returns the chosen card
        :return:
        """
        try:
            card = random.choice(self.cards)
            self.cards.remove(card)
            self.played_cards.append(card)
            return card
        except IndexError:
            print("No cards in card list")
            return None

    def reset_cards(self):
        """
        Reset cards to initial state, remove all played cards
        :return:
        """
        self.played_cards = []
        self.cards = []
        self.populate_cards()

    def shuffle_check(self):
        """
        Reset the card manager if the amount of remaining cards is less than the shuffle limit
        """
        if len(self.cards) < self.shuffle_limit:
            self.reset_cards()
