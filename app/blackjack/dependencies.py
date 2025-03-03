from app.services.game_service import GameService, GAME_SERVICE


def get_game_service() -> GameService:
    return GAME_SERVICE