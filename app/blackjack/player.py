from starlette.websockets import WebSocket


class Player:
    def __init__(self, player_id: str, player_nickname: str, websocket: WebSocket, points: int):
        self.player_id: str = player_id
        self.player_nickname: str = player_nickname
        self.socket: WebSocket = websocket
        self.points: int = points
        self.hand: list = []
        self.hand_value = 0
        self.play_state = "Waiting"

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
