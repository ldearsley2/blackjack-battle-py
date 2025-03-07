from app.blackjack.deck import VALUE_DICT

class CardCalculator:
    """
    CardCalculator is responsible for calculating the hand value for a given hand.
    """

    def __init__(self, max_hand: int):
        self.max_hand = max_hand

    def get_card_value(self, card: str) -> int:
        """
        Get card value from VALUE_DICT
        """
        return VALUE_DICT[card[:-1]]

    def get_hand_value_no_ace(self, hand: list[str]) -> int:
        """
        Get the card value for a given hand
        """
        hand_value = 0
        for card in hand:
            hand_value += self.get_card_value(card)[0]
        return hand_value

    def bust_check(self, hand_value: int) -> int:
        """
        Check if given hand value exceeds the max hand
        """
        if hand_value > self.max_hand:
            return -1
        return hand_value


    def get_hand_value_with_ace(self, hand: list[str]) -> int:
        """
        Calculate hand value that contains aces
        """
        hand_value = 0
        aces = []
        values = [self.get_card_value(card) for card in hand]

        # Split aces into seperate array
        for index, value in enumerate(values):
            if value[0] == 1:
                aces.append(value)
                values.pop(index)

        # Get value of all non-ace cards
        non_ace_value = 0
        for v in values:
            non_ace_value += v[0]

        if len(aces) == 1:
            small_val = non_ace_value + aces[0][0]
            large_val = non_ace_value + aces[0][1]
            if large_val <= self.max_hand:
                return large_val
            else:
                return small_val

        return hand_value