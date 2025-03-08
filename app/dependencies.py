from fastapi import Depends

from app.blackjack.card_manager import CardManager
from app.blackjack.game import BlackJackGame
from app.services.game_service import GameService, GAME_SERVICE


def get_game_service() -> GameService:
    return GAME_SERVICE


def get_blackjack_game(
    game_service: GameService = Depends(get_game_service),
) -> BlackJackGame:
    return BlackJackGame(CardManager(decks=1), game_service)
