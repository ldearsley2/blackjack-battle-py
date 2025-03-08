from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.routes import router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Starting Blackjack-Battle")

    yield

    print("Shutting down BB")


app = FastAPI(title="Blackjack-Battle", lifespan=lifespan)
app.include_router(router)


def start():
    """
    Start a uvicorn server using the FastAPI app
    :return:
    """
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)


def start_dev():
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)
