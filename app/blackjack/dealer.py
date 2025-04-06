class Dealer:
    def __init__(self, stop_limit: int):
        self.cards: list[str] = []
        self.stop_limit: int = stop_limit

    def get_cards(self):
        """
        Get dealers current cards
        """
        return self.cards

    def get_stop_limit(self):
        """
        Get dealer stop limit
        """
        return self.stop_limit

    def add_to_cards(self, card: str):
        """
        Add card to hand
        """
        self.cards.append(card)

    def remove_cards(self):
        """
        Remove all cards in dealers hand
        """
        self.cards = []
