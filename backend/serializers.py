"""
The bridge between what comes in through the frontend
and what comes out of the backend.
"""

from abc import ABC, abstractmethod
from backend.choices import PysweeperItemTypes
from backend.data.connector import PysweeperDataConnector
from datetime import datetime
from backend.exceptions import PysweeperGameDoesNotExist
import logging
from backend.pysweeper import GameBoard, Square, Scoreboard

logger = logging.getLogger("pysweeper")


class PysweeperSerializer(ABC):
    """The contract for all serializers"""

    def __init__(self, data_source: PysweeperDataConnector):
        """PysweeperSerializer contructor: accepts connector"""

    @abstractmethod
    def load(data: dict) -> GameBoard | Scoreboard:
        """load method"""

    @abstractmethod
    def save(game: GameBoard):
        """save method"""

    @abstractmethod
    def delete(name: str):
        """delete method"""


class PysweeperGameSerializer(PysweeperSerializer):
    def __init__(self, db: PysweeperDataConnector):
        self.db = db

    def load(self, name: str) -> GameBoard:
        if type(name) is not str:
            raise TypeError(f"Expected a string, but got {type(name)}")

        logger.debug(f"Serializing game: name={name}")
        game_row: dict = self.db.read_one(
            PysweeperItemTypes.GAME, filter={"name": name}
        )
        if not game_row:
            raise PysweeperGameDoesNotExist(f"Game does not exist: {name}")

        logger.debug(f"Building board: name={name}")
        # TODO: can i rescue if not the board fails to instantiate?
        game_record = self.db.GAME_MODEL(game_row).obj()
        board = GameBoard(**game_record)

        logger.debug(f"Retrieving Squares: name={name}")
        square_records: list[dict] = self.db.read_many(
            PysweeperItemTypes.SQUARE, filter={"name": name}
        )

        rows = set()
        columns = set()
        for square in square_records:
            rows.add(square.get("pos_x"))
            columns.add(square.get("pos_y"))

        grid = [[None for _ in rows] for _ in columns]

        for _square in square_records:
            square = self.db.SQUARE_MODEL(_square)
            built_square = Square(**square.obj())
            grid[built_square.pos_x][built_square.pos_y] = built_square

        board.rows = grid

        logger.debug(f"Done building board: name={name}")
        return board

    def save(self, game: GameBoard):
        # TODO: maybe have this return a save status (ie success or fail)
        # TODO: Hallucinated game.name: GameBoard needs attr added

        # Pass in all attributes except the list of rows
        game_attrs = game.__dict__
        found_game: dict = self.db.read_one(
            PysweeperItemTypes.GAME, filter={"name": game_attrs.get("name")}
        )

        if found_game:
            # TODO: also save the squares
            # logger.info(f"Updating board: name={game.name}")
            # TODO: figure out a way to only operate on squares that changed
            for row in game.rows:
                for square in row:
                    _square_record = square.__dict__
                    square_record = self.db.SQUARE_MODEL(_square_record)
                    self.db.update(
                        item=PysweeperItemTypes.SQUARE,
                        filter={
                            "name": game.name,
                            "pos_x": square.pos_x,
                            "pos_y": square.pos_y,
                        },
                        data=square_record.db(game.name),
                    )

            # TODO: figure out how start and end times figure into this
            # TODO: add tests for adding end date
            if game_attrs.get("game_over"):
                game_over_time = str(datetime.now())
                game_attrs["end_date"] = game_over_time
                logger.info(f"Game Over: name={game.name}, time={game_over_time}")

            game_row = self.db.GAME_MODEL(game_attrs)

            logger.debug(f"Updating game: name={game.name}")
            self.db.update(
                item=PysweeperItemTypes.GAME,
                filter={"name": game.name},
                data=game_row.db(),
            )
        else:
            # TODO: add time and dates to data
            name = game_attrs.get("name")

            logger.info(f"Saving new game: name={name}")
            for row in game.rows:
                for square in row:
                    square_record = square.__dict__
                    square_record = self.db.SQUARE_MODEL(square_record)
                    self.db.create(PysweeperItemTypes.SQUARE, square_record.db(name))

            game_attrs["start_date"] = str(datetime.now())
            game_attrs["end_date"] = None
            game_row = self.db.GAME_MODEL(game_attrs)
            self.db.create(PysweeperItemTypes.GAME, game_row.db())

    def delete(self, name: str):
        # TODO: make sure there's no chance that there are orphan squares
        # if a game gets deleted, but an error happens, the squares can
        # get stuck in the db.
        game_exists = self.db.read_one(PysweeperItemTypes.GAME, filter={"name": name})
        if game_exists:
            logger.debug(f"Deleting game: name={name}")
            self.db.destroy(PysweeperItemTypes.GAME, filter={"name": name})

            # logger.info(f"Deleting squares: name={name}")
            self.db.destroy(PysweeperItemTypes.SQUARE, filter={"name": name})
        else:
            raise PysweeperGameDoesNotExist(f"Game does not exist with name: {name}")


# TODO: Should probably make a square serializer
# include methods for serializing many or one at a time

# TODO: should probably make a response serializer

# TODO: should probably make a request serializer


class PysweeperScoreboardSerializer(PysweeperSerializer):
    # TODO: build this...
    def __init__():
        """Pysweeper scoreboard"""

    def load():
        """load method"""

    def save():
        """save method"""

    def delete():
        """delete method"""
