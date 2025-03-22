from fastapi import Depends

from app.blackjack.game import BlackJackGame
from app.services.game_service import GameService, GAME_SERVICE
from app.services.state_service import StateService, STATE_SERVICE


def get_game_service() -> GameService:
    return GAME_SERVICE


def get_state_service() -> StateService:
    return STATE_SERVICE

def get_blackjack_game(state_service: StateService = Depends(get_state_service)) -> BlackJackGame:
    return BlackJackGame(state_service, 1, 20, 21)

