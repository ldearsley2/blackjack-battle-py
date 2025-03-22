import uuid

from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket

from app.blackjack.game import BlackJackGame
from app.dependencies import get_state_service, get_game_service, get_blackjack_game
from app.services.state_service import StateService

socket_router = APIRouter()
fe_connections: list[WebSocket] = []
game_service = get_game_service()


@socket_router.websocket("/ws")
async def websocket_endpoint(
        websocket: WebSocket, state_service: StateService = Depends(get_state_service)
):
    """
    Websocket for front end connections, provides game state at connection
    """

    await websocket.accept()

    fe_connections.append(websocket)
    print("New front-end client connected!")

    try:
        await websocket.send_json(state_service.get_game_state())
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")

    except Exception as e:
        print(f"Websocket error: {e}")


@socket_router.websocket("/connect")
async def connect(
        websocket: WebSocket,
        blackjack_game: BlackJackGame = Depends(get_blackjack_game)
):
    """
    Websocket for blackjack player connections
    """
    await websocket.accept()
    print("New blackjack player connected")

    try:
        while True:
            data = await websocket.receive_json()

            if data["action"] == "connect":
                player_id = str(uuid.uuid4())
                blackjack_game.add_player(player_id=player_id, player_nickname=data["player_nickname"], player_socket=websocket)
                await websocket.send_json({
                    "action": "connected",
                    "player_id": player_id
                })
                print("added player")

            if data["action"] == "turn":
                action, player_id = data["action"], data["player_id"]

            print(data)

    except Exception as e:
        print(f"Websocket error: {e}")


async def send_turn(player_id: str, turn_data):
    players = game_service.get_players()
    websocket = players[player_id].player_socket
    await websocket.send_json(turn_data)

    try:
        response = await websocket.receive_json()
        action = response.get("action")
        return action
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None



async def broadcast_update(update: dict):
    """
    Send an update to all connected websockets, remove disconnected
    """
    remove_connections = []

    for connection in fe_connections:
        try:
            await connection.send_json(update)
            print("Sent update to FE")
        except RuntimeError as e:
            print("Tried to send message to disconnected connection")
            print(e)
            remove_connections.append(connection)

    for connection in remove_connections:
        fe_connections.remove(connection)
