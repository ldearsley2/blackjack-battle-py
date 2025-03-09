from fastapi import APIRouter, Depends

from app.blackjack.card_calculator import CardCalculator
from app.blackjack.card_manager import CardManager
from app.dependencies import get_game_service
from app.blackjack.game import BlackJackGame
from app.models.connection import Connection
from app.services.game_service import GameService

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Welcome to blackjack battle!"}


@router.post("/connect")
async def connect(
    connection: Connection, game_service: GameService = Depends(get_game_service)
):
    """
    Connection endpoint for blackjack players
    """
    player_url: str = connection.url
    player_id = game_service.add_player(player_url)
    print(f"Player connected with URL: {player_url}")
    return {"player_id": player_id}


@router.post("/play-round")
async def play_round(game_service: GameService = Depends(get_game_service)):
    """
    Run a full round of blackjack
    """
    card_manager = CardManager(decks=1, shuffle_limit=20)
    card_calc = CardCalculator(max_hand=21)
    blackjack_game = BlackJackGame(card_manager=card_manager, card_calc=card_calc)

    # Wait for connection check
    await game_service.connection_check()

    blackjack_game.add_players(game_service)

    while blackjack_game.players:
        blackjack_game.play_round()
