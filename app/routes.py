from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.blackjack.card_calculator import CardCalculator
from app.blackjack.card_manager import CardManager
from app.dependencies import get_game_service, get_state_service
from app.blackjack.game import BlackJackGame
from app.models.connection import Connection
from app.services.game_service import GameService
from app.services.state_service import StateService

router = APIRouter()
active_connections: list[WebSocket] = []


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
        player_id = game_service.add_player(connection.url)
        return {"player_id": player_id}
    else:
        return {"Message": "User is already connected with given URL"}


@router.post("/play-round")
async def play_round(game_service: GameService = Depends(get_game_service),
                     state_service: StateService = Depends(get_state_service)):
    """
    Run a full round of blackjack
    """
    card_manager = CardManager(decks=1, shuffle_limit=20)
    card_calc = CardCalculator(max_hand=21)
    blackjack_game = BlackJackGame(card_manager=card_manager, card_calc=card_calc, state_service=state_service)

    # Wait for connection check
    await game_service.live_check()

    blackjack_game.add_players(game_service.get_players())

    while blackjack_game.players:
        await blackjack_game.play_round()
        await broadcast_update(state_service.get_game_state())


# Websocket functionality
async def broadcast_update(update: dict):
    """
    Send an update to all connected websockets, remove disconnected
    """
    remove_connections = []

    for connection in active_connections:
        # Insert the json object to send
        try:
            await connection.send_json(update)
            print("Sent update to FE")
        except RuntimeError as e:
            print("Tried to send message to disconnected connection")
            print(e)
            remove_connections.append(connection)

    for connection in remove_connections:
        active_connections.remove(connection)



@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,
                             state_service: StateService = Depends(get_state_service)):
    """
    Websocket for connected front ends, send current state of blackjack game
    """
    await websocket.accept()

    active_connections.append(websocket)
    print("A new client has connect with websocket")

    try:
        await websocket.send_json(state_service.get_game_state())
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")

    except Exception as e:
        print(f"Websocket error: {e}")



