import uvicorn
import logging
from fastapi import FastAPI, Body, HTTPException
from typing import Any, Dict
from backend.data.sqlite.connector import PysweeperSQLiteData
from backend.serializers import PysweeperGameSerializer
from backend.validators import PysweeperValidators
from backend.exceptions import PysweeperValidationError, PysweeperValueError
from backend.game_service import PysweeperGameService

from fastapi.middleware.cors import CORSMiddleware

# TODO: make an "environment loader" for taking in settings (.envs)
# TODO: instantiate logger... (might make a logger handler)
logger = logging.getLogger("pysweeper")
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(
        filename="pysweeper.log", mode="a", encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    console_formatter = logging.Formatter(fmt="[%(levelname)s] %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
connector = PysweeperSQLiteData("test2.db")
serializer = PysweeperGameSerializer(connector)
service = PysweeperGameService(serializer)
validator = PysweeperValidators()


# new game
@app.post("/game/new")
def new_game(payload: Dict[Any, Any] = Body(...)):
    """Creates new game"""
    # TODO: lots of duplication in this try except structure
    # should probably handle this in a response serializer
    try:
        validated_payload = validator.validated(payload)
        name = validated_payload.get("name")
        difficulty = validated_payload.get("difficulty")
        service.new(name=name, difficulty=difficulty)
        # TODO: don't like return "null"
        return
    except (PysweeperValueError, PysweeperValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # TODO: log internal exception with logger
        raise HTTPException(status_code=500, detail=str(e))


# delete game
@app.post("/game/delete")
def delete_game(payload: Dict[Any, Any] = Body(...)):
    """Deletes existing game"""
    try:
        validated_payload = validator.validated(payload)
        name = validated_payload.get("name")
        service.delete(name)
        return
    except (PysweeperValidationError, PysweeperValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# play
@app.get("/game/play/{player}")
def play_game(player):
    """Returns current board state"""
    try:
        # TODO: need validation here
        game = service.get(player)
        return game
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/game/square/{player}")
def square(player, payload: Dict[Any, Any] = Body(...)):
    """Interacts with square"""
    try:
        payload["name"] = player
        validated_payload = validator.validated(payload)
        if validated_payload.get("flag"):
            service.set_flag(**validated_payload)
            return
        # del validated_payload["flag"]
        else:
            revealed = service.square(**validated_payload)
            return revealed  # revealed squares
    except (PysweeperValueError, PysweeperValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# scoreboard
@app.get("/scoreboard")
def scoreboard():
    """Returns scoreboard data"""


# home
@app.get("/")
def home():
    return


if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
