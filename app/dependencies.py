from app.services.game_service import GameService, GAME_SERVICE
from app.services.state_service import StateService, STATE_SERVICE


def get_game_service() -> GameService:
    return GAME_SERVICE


def get_state_service() -> StateService:
    return STATE_SERVICE
