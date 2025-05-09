from enum import Enum


class PlayStates(Enum):
    WAITING = "Waiting"
    PLAYING = "Playing"
    BUSTED = "Busted"
    DREW = "Drew"
    STAND = "Stand"
    WIN = "Win"
    LOSS = "Loss"
    TIMEOUT = "Timeout"
    CONNECTION_LOSS = "Connection lost"
    DISQUALIFIED = "Disqualified"


class Player:
    def __init__(self, player_id: str, player_nickname: str, url: str, points: int):
        self.player_id: str = player_id
        self.player_nickname: str = player_nickname
        self.url: str = url
        self.points: int = points
        self.hand: list = []
        self.hand_value = 0
        self.play_state: PlayStates = PlayStates.WAITING
        self.bet_amount: int = 0

    def get_points(self):
        return self.points

    def add_points(self, points: int):
        self.points += points

    def remove_points(self, points: int):
        self.points -= points

    def set_bet_amount(self, points: int):
        """
        Set the amount of points the player is betting.
        """
        self.points -= points
        self.bet_amount += points

    def reset_bet_amount(self):
        self.bet_amount = 0

    def get_bet_amount(self):
        return self.bet_amount

    def add_to_hand(self, card: str):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def get_play_state(self):
        return self.play_state.value

    def set_play_state(self, state: PlayStates):
        self.play_state = state

    def round_reset(self):
        """
        Reset values for next round of blackjack
        """
        self.set_play_state(PlayStates.WAITING)
        self.reset_bet_amount()
        self.clear_hand()
        self.hand_value = 0
