from app.blackjack.deck import VALUE_DICT


class CardCalculator:
    """
    CardCalculator is responsible for calculating the hand value for a given hand.
    """

    def __init__(self, max_hand: int):
        self.max_hand = max_hand

    def get_card_value(self, card: str) -> list[str]:
        """
        Get card value from VALUE_DICT
        """
        return VALUE_DICT[card[:-1]]

    def has_busted(self, hand_value: int) -> bool:
        """
        Check if given hand value exceeds the max hand
        """
        if hand_value > self.max_hand:
            return True
        return False

    def contains_ace(self, hand: list[str]) -> bool:
        """
        Check if given hand contains an ace card
        """
        for card in hand:
            if card[:1] == "A":
                return True
        return False

    def get_hand_value_no_ace(self, hand: list[str]) -> int:
        """
        Get the card value for a given hand
        """
        hand_value = 0
        for card in hand:
            hand_value += self.get_card_value(card)[0]
        return hand_value

    def get_hand_value_with_ace(self, hand: list[str]) -> int:
        """
        Calculate hand value that contains aces
        """
        aces = []
        values = [self.get_card_value(card) for card in hand]

        # Split aces into separate array
        for value in values[:]:
            if value[0] == 1:
                aces.append(value)
                values.remove(value)

        # Get value of all non-ace cards
        non_ace_value = 0
        for v in values:
            non_ace_value += v[0]

        # Handle singular ace hands
        if len(aces) == 1:
            small_val = non_ace_value + int(aces[0][0])
            large_val = non_ace_value + int(aces[0][1])
            if large_val <= self.max_hand:
                return large_val
            else:
                return small_val

        ace_sum = 0
        for ace in aces[1:]:
            ace_sum += ace[0]

        overall = non_ace_value + ace_sum
        if overall + int(aces[0][1]) > self.max_hand:
            return overall + int(aces[0][0])
        else:
            return overall + int(aces[0][1])

    def get_hand_value(self, hand: list[str]) -> int:
        if self.contains_ace(hand):
            score = self.get_hand_value_with_ace(hand)
        else:
            score = self.get_hand_value_no_ace(hand)
        return score
