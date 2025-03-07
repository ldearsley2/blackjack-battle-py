from fastapi import APIRouter, Depends

from app.blackjack.dependencies import get_game_service
from app.blackjack.game import BlackJackGame
from app.models.connection import Connection
from app.services.game_service import GameService

router = APIRouter()


@router.get("/")
async def root():
    print(get_game_service().connected_players)
    return {"message": "Welcome to blackjack battle!"}


@router.post("/connect")
async def connect(
    connection: Connection, game_service: GameService = Depends(get_game_service)
):
    player_url: str = connection.url
    player_id = game_service.add_player(player_url)
    return {"player_id": player_id}


@router.post("/play_round")
async def play_round(
    game_service: GameService = Depends(get_game_service),
    blackjack_game: BlackJackGame = Depends(),
):
    game_service.connection_check()
    blackjack_game.play_round()
