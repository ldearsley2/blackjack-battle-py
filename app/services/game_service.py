import requests

class GameService:
    """
    GameService SINGLETON
    Maintains connected players to current session
    """
    def __init__(self):
        self.connected_players: dict[int, str] = {}

    def add_player(self, player_url: str) -> int:
        """
        Add player to connected_players
        :param player_url:
        :return:
        """
        player_id = len(self.connected_players)+1
        self.connected_players[player_id] = player_url
        return player_id

    def remove_player(self, player_id: int):
        """
        Remove played from connected_players
        :param player_id:
        :return:
        """
        try:
            self.connected_players.pop(player_id)
        except KeyError:
            raise KeyError(f"Player: {player_id} is not a connected player")

    def connection_check(self):
        """
        Sends connected checks to all connections, connection should return player_id
        :return:
        """
        for k, v in self.connected_players:
            response = requests.get(f"{v}connection_check")
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    if json_data["player_id"] == v:
                        continue
                    else:
                        self.remove_player(k)
                except ValueError:
                    print(f"player_id not found in response")



GAME_SERVICE = GameService()
