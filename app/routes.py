from fastapi import APIRouter, Depends

from app.blackjack.card_calculator import CardCalculator
from app.blackjack.card_manager import CardManager
from app.dependencies import get_game_service, get_state_service
from app.blackjack.game import BlackJackGame
from app.models.connection import Connection
from app.services.game_service import GameService
from app.services.state_service import StateService
from app.sockets import broadcast_update

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
    if game_service.can_connect(connection.url):
        player_id = game_service.add_player(player_nickname=connection.nickname, player_url=connection.url)
        return {"player_id": player_id}
    else:
        return {"Message": "User is already connected with given URL"}


@router.post("/play-round")
async def play_round(
    game_service: GameService = Depends(get_game_service),
    state_service: StateService = Depends(get_state_service),
):
    """
    Run a full round of blackjack
    """
    blackjack_game = BlackJackGame(
         state_service=state_service, decks=1, shuffle_limit=20, max_hand=21
    )

    # Wait for connection check
    await game_service.live_check()

    blackjack_game.add_players(game_service.get_players())

    while blackjack_game.players:
        await blackjack_game.play_round()
        await broadcast_update(state_service.get_game_state())
        await game_service.live_check()

