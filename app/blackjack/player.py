class Player:
    def __init__(self, url: str, points: int):
        self.url: str = url
        self.points: int = points

    def add_points(self, points: int):
        self.points += points

    def remove_points(self, points: int):
        if points > self.points:
            self.points = 0
        self.points -= points
