from app.blackjack.player import Player

class BlackjackLogger:

    def log_current_state(self, players: list[Player]):
        print("| Player_id | Hand | Status | Points |")
        for p in players:
            print(f"| {p.player_id} | {p.hand} | {p.play_state} | {p.points} |")

    def log_round_end(self, player: Player):
        print("| Player_id | Hand | Status | Points |")
        print(
            f"| {player.player_id} | {player.hand} | {player.play_state} | {player.points} |"
        )

