class Player:
    def __init__(self, player_id: str, url: str, points: int):
        self.player_id: str = player_id
        self.url: str = url
        self.points: int = points
        self.hand: list = []
        self.play_state = ""

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
