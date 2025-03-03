class GameService:
    def __init__(self):
        self.connected_players: dict[int, str] = {}

    def add_player(self, player_url: str) -> int:
        player_id = len(self.connected_players)+1
        self.connected_players[player_id] = player_url
        return player_id

    def remove_player(self, player_id: int):
        try:
            self.connected_players.pop(player_id)
        except KeyError:
            raise KeyError(f"Player: {player_id} is not a connected player")

GAME_SERVICE = GameService()
