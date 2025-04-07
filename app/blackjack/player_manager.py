from app.blackjack.player import Player, PlayStates
from app.services.game_service import GSPlayer


class PlayerManager:
    def __init__(self):
        self.players: list[Player] = []
        self.finished_players: list[Player] = []

    def add_players(self, players_dict: dict[str, GSPlayer]):
        """
        Add connected players from the game_service
        """
        for player_id, gsplayer in players_dict.items():
            self.players.append(
                Player(
                    player_id=str(player_id),
                    player_nickname=gsplayer.player_nickname,
                    url=gsplayer.player_url,
                    points=10,
                )
            )

    def set_players_status(self, dealer_score: int):
        """
        Set player statuses based on dealer's final score
        """
        for player in self.players:
            if player.get_play_state() == PlayStates.BUSTED.value:
                continue
            if dealer_score == player.hand_value:
                player.set_play_state(PlayStates.DREW)
            if dealer_score > player.hand_value:
                player.set_play_state(PlayStates.BUSTED)

    def adjust_player_points(self):
        """
        Adjust points for all connected blackjack players
        """
        for player in self.players:
            if player.get_play_state() == PlayStates.DREW.value:
                player.add_points(player.get_bet_amount())
                continue
            if not player.get_play_state() == PlayStates.BUSTED.value:
                player.add_points(player.get_bet_amount() * 2)
                player.set_play_state(PlayStates.WIN)
            else:
                player.set_play_state(PlayStates.LOSS)
                if player.points <= 0:
                    self.finished_players.append(player)
                    self.players.remove(player)
