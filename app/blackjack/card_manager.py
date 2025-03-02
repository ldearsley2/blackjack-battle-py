from app.blackjack.deck import DECK


class CardManager:
    def __init__(self, decks: int):
        self.cards: list = []
        self.decks: int = decks

    def populate_cards(self):
        for i in range(self.decks):
            self.cards.extend(DECK)
