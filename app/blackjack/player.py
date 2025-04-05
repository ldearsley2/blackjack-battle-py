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


class Player:
    def __init__(self, player_id: str, player_nickname: str, url: str, points: int):
        self.player_id: str = player_id
        self.player_nickname: str = player_nickname
        self.url: str = url
        self.points: int = points
        self.hand: list = []
        self.hand_value = 0
        self.play_state: PlayStates = PlayStates.WAITING

    def add_points(self, points: int):
        self.points += points

    def remove_points(self, points: int):
        if points > self.points:
            self.points = 0
            return
        self.points -= points

    def add_to_hand(self, card: str):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def get_play_state(self):
        return self.play_state.value

    def set_play_state(self, state: PlayStates):
        self.play_state = state
