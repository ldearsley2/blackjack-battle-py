import uuid
from pathlib import Path

import requests
from fastapi import APIRouter, Depends

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
        player_id = game_service.add_player(
            player_nickname=connection.nickname, player_url=connection.url
        )
        return {"player_id": player_id}
    else:
        return {"Message": "User is already connected with given URL"}


@router.post("/manual-connect")
async def manual_connect(game_service: GameService = Depends(get_game_service)):
    """
    Manually connect all players within env file
    """
    env_path = Path(__file__).parent.parent / ".env"
    with open(env_path, "r") as file:
        for line in file:
            if line.startswith("_"):
                url = line.strip().split("=")[1]
                player_id = str(uuid.uuid4())
                response = requests.get(
                    url=f"{url}/connect", json={"player_id": player_id}
                )
                if response.json()["player_id"] == player_id:
                    game_service.add_player(
                        player_nickname=response.json()["nickname"], player_id=player_id, player_url=url
                    )
                else:
                    print("Returned wrong player_id")


@router.post("/play-round")
async def play_round(
    game_service: GameService = Depends(get_game_service),
    state_service: StateService = Depends(get_state_service),
):
    """
    Run a full round of blackjack
    """
    if state_service.in_progress:
        return {"Message": "Game already in progress"}

    state_service.in_progress = True
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

    state_service.in_progress = False
