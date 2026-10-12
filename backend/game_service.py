from abc import ABC, abstractmethod
from backend.data.connector import PysweeperDataConnector
from backend.serializers import PysweeperGameSerializer
from backend.choices import PysweeperItemTypes
from backend.exceptions import PysweeperValidationError, PysweeperValueError
import logging
from backend.pysweeper import GameBoard, Square
from backend.serializers import (
    PysweeperSerializer,
    PysweeperScoreboardSerializer,
)

logger = logging.getLogger("pysweeper")


class GameService(ABC):
    """Game Service contract"""

    def __init__(self, repository):
        """Build game service using repository"""

    @abstractmethod
    def new(self, *args):
        """Create a new game based on args"""

    @abstractmethod
    def delete(self, *args):
        """Delete specific game"""

    @abstractmethod
    def get(self, *args):
        """Get existing game"""


class PysweeperGameService:
    """PysweeperGameService"""

    def __init__(self, serializer: PysweeperGameSerializer):
        """constructor"""
        self.serializer = serializer

    def new(self, name: str, difficulty: int):
        """Create new game"""
        game = GameBoard(name=name, difficulty=difficulty)
        game.buildBoard()
        logger.info(f"Created new game: name={name}, difficulty={difficulty}")
        self.serializer.save(game)

    def delete(self, name: str):
        """Delete game"""
        logger.info(f"Deleting game: name={name}")
        self.serializer.delete(name)

    def get(self, name: str) -> dict:
        """Get current game state (squares & time)"""
        # TODO: This is super not great...
        # this will probably be the reason i make the repo
        logger.info(f"Getting game data: name={name}")
        game: dict = self.serializer.db.read_one(
            PysweeperItemTypes.GAME, filter={"name": name}
        )
        name = game.get("name")
        # TODO: this wont return flags
        # because flags and clickable are usually simultaneously false
        logger.info(f"Getting revealed squares: name={name}")
        revealed_squares = self.serializer.db.read_many(
            PysweeperItemTypes.SQUARE, filter={"name": name, "revealed": True}
        )
        logger.info(f"Getting flagged squares: name={name}")
        flagged_squares = self.serializer.db.read_many(
            PysweeperItemTypes.SQUARE, filter={"name": name, "flag": True}
        )
        full_squares = (
            revealed_squares + flagged_squares
        )  # TODO: what if one or both return none
        trimmed_squares = []
        logger.info(f"Building game data payload: name={name}")
        for sq in full_squares:
            _sq = self.serializer.db.SQUARE_MODEL(sq).obj()
            base = {"pos_x": _sq["pos_x"], "pos_y": _sq["pos_y"]}
            if _sq["flag"]:
                trimmed_squares.append(base | {"flag": _sq["flag"]})
            else:
                trimmed_squares.append(base | {"number": _sq["number"]})

        payload = {
            "name": name,
            "difficulty": game.get("difficulty"),
            "start_date": game.get("start_date"),
            "squares": trimmed_squares,
        }
        return payload

    def set_flag(self, name: str, x: int, y: int, flag: bool):
        """Set flag value to exactly what is passed"""
        game = self.serializer.load(name)
        square = game.getSquare(x, y)
        square.flag = flag
        self.serializer.save(game)

    def toggle_flag(self, name: str, x: int, y: int):
        """Places flag on square"""
        game = self.serializer.load(name)
        square = game.getSquare(x, y)
        flag_status = int(square.flag)
        square.flag = bool(1 - flag_status)
        self.serializer.save(game)

    def square(self, name: str, x: int, y: int):
        """interacts with square"""
        game: GameBoard = self.serializer.load(name)
        revealed: list[Square] = game.click(x, y)
        if not revealed:
            return {"game_over": game.game_over, "revealed": []}
        # self.serializer.save(game)
        # TODO: should probably let a response serializer handle this
        if game.game_over:
            logger.info(f"Detected Game Over for {name}")
            game_over_squares = []
            for sq in revealed:
                sq.revealed = True
                bomb_or_number_key = "bomb" if sq.bomb else "number"
                bomb_or_number_value = sq.bomb if sq.bomb else sq.number
                game_over_squares.append(
                    {
                        "pos_x": sq.pos_x,
                        "pos_y": sq.pos_y,
                        bomb_or_number_key: bomb_or_number_value,
                    }
                )
            # TODO: record game in scoreboard, delete game
            self.serializer.save(game)
            return {
                "game_over": game.game_over,
                "revealed": game_over_squares,
            }
        else:
            self.serializer.save(game)
            return {
                "game_over": game.game_over,
                "revealed": [
                    {"pos_x": sq.pos_x, "pos_y": sq.pos_y, "number": sq.number}
                    for sq in revealed
                ],
            }
