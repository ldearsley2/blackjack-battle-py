class StateService:
    """
    Maintain a game state to update front-end connections
    """
    def __init__(self):
        self.game_state = {
        }
        self.in_progress = False

    def set_game_state(self, state: dict):
        self.game_state = state

    def get_game_state(self) -> dict:
        return self.game_state


STATE_SERVICE = StateService()
