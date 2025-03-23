from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket

from app.dependencies import get_state_service
from app.services.state_service import StateService

socket_router = APIRouter()
active_connections: list[WebSocket] = []

@socket_router.websocket("/ws")
async def websocket_endpoint(
        websocket: WebSocket, state_service: StateService = Depends(get_state_service)
):
    """
    Websocket for front end connections, provides game state at connection
    """

    await websocket.accept()
    active_connections.append(websocket)

    try:
        await websocket.send_json(state_service.get_game_state())
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")

    except Exception as e:
        print(f"Websocket error: {e}")


async def broadcast_update(update: dict):
    """
    Send an update to all connected websockets, remove disconnected
    """
    remove_connections = []

    for connection in active_connections:
        try:
            await connection.send_json(update)
        except RuntimeError as e:
            print(e)
            remove_connections.append(connection)

    for connection in remove_connections:
        active_connections.remove(connection)
