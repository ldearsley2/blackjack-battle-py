class StateService:
    def __init__(self):
        pass

        self.game_state = {}

    def set_game_state(self, state: dict):
        self.game_state = state

    def get_game_state(self) -> dict:
        return self.game_state

STATE_SERVICE = StateService()