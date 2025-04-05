import requests


class GSPlayer:
    def __init__(self, player_nickname: str, player_url: str):
        self.player_nickname: str = player_nickname
        self.player_url: str = player_url


class GameService:
    """
    GameService SINGLETON
    Maintains connected players to current session
    """

    def __init__(self):
        self.connected_players: dict[str, GSPlayer] = {}

    def add_player(self, player_nickname: str, player_id: str, player_url: str) -> str:
        """
        Add player to connected_players
        :param player_nickname:
        :param player_id:
        :param player_url:
        :return:
        """
        self.connected_players[player_id] = GSPlayer(
            player_nickname=player_nickname, player_url=player_url
        )
        return player_id

    def remove_player(self, player_id: str):
        """
        Remove played from connected_players
        :param player_id:
        :return:
        """
        try:
            self.connected_players.pop(player_id)
        except KeyError:
            raise KeyError(f"Player: {player_id} is not a connected player")

    def get_players(self) -> dict[str, GSPlayer]:
        """
        Return a dictionary of player_id to GSPlayer
        """
        return self.connected_players

    async def live_check(self):
        """
        Sends connected checks to all connections, connection should return player_id
        :return:
        """
        failed = []
        for player_id, gsplayer in self.connected_players.items():
            try:
                response = requests.get(
                    f"{gsplayer.player_url}/connection-check", timeout=10
                )
                if response.status_code == 200:
                    try:
                        json_data = response.json()
                        if json_data["player_id"] == player_id:
                            continue
                        else:
                            failed.append(player_id)
                    except ValueError:
                        print("player_id not found in response")
            except requests.Timeout:
                print(f"{player_id} did not respond to live check")
                failed.append(player_id)
            except requests.ConnectionError:
                print(f"{player_id} lost connection")
                failed.append(player_id)

        for player_id in failed:
            self.remove_player(player_id)

    def can_connect(self, check_url: str) -> bool:
        """
        Check the given url is not already connected to the game_service
        """
        for player_id, gsplayer in self.connected_players.items():
            if gsplayer.player_url == check_url:
                return False
        return True


GAME_SERVICE = GameService()
