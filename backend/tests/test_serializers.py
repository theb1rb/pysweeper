from backend.choices import PysweeperItemTypes
from backend.data.connector import PysweeperDataConnector

from backend.data.sqlite.models import SQLiteGameRecordModel, SQLiteSquareRecordModel
from backend.exceptions import PysweeperValueError, PysweeperGameDoesNotExist
from backend.serializers import PysweeperGameSerializer
from backend.settings import MAX_DIFFICULTY
import logging
from backend.pysweeper import GameBoard, Square
import unittest
from unittest.mock import MagicMock, patch

logger = logging.getLogger("pysweeper")


class MockPysweeperGameRecordModel(SQLiteGameRecordModel):
    """Mock GameRecordModel"""


class MockPysweeperSquareRecordModel(SQLiteSquareRecordModel):
    """Mock SquareRecordModel"""


class MockPysweeperDataConnector(PysweeperDataConnector):
    GAME_MODEL = MockPysweeperGameRecordModel
    SQUARE_MODEL = MockPysweeperSquareRecordModel

    def __init__(self):
        """Mock Pysweeper Data Connector"""
        self.board_records = {
            "good_board": {
                "name": "good_board",
                "difficulty": 1,
                "game_over": False,
                "start_date": "2026-10-03 12:00pm",
                "end_date": None,
            },
            "good_board_bad_squares": {
                "name": "good_board_bad_squares",
                "difficulty": 1,
                "game_over": False,
                "start_date": "2026-10-03 12:00pm",
                "end_date": None,
            },
            "bad_name_type_board": {
                "name": 123,
                "difficulty": 1,
                "game_over": False,
                "start_date": "2026-10-03 12:00pm",
                "end_date": None,
            },
            "bad_name_length_board": {
                "name": "abcdefghijklmnopqrstuvwxyz",
                "difficulty": 1,
                "game_over": False,
                "start_date": "2026-10-03 12:00pm",
                "end_date": None,
            },
            "bad_difficulty_type_board": {
                "name": "bad_difficulty_board",
                "difficulty": "bad_difficulty",
                "game_over": False,
                "start_date": "2026-10-03 12:00pm",
                "end_date": None,
            },
            "bad_difficulty_value_board": {
                "name": "bad_difficulty_value_board",
                "difficulty": 9001,
                "game_over": False,
                "start_date": "2026-10-03 12:00pm",
                "end_date": None,
            },
        }
        self.square_records = {
            "good_board": [
                {
                    "name": "good_board",
                    "pos_x": 0,
                    "pos_y": 0,
                    "bomb": False,
                    "flag": False,
                    "number": 0,
                    "revealed": False,
                    "id": 1,
                },
                {
                    "name": "good_board",
                    "pos_x": 0,
                    "pos_y": 1,
                    "bomb": False,
                    "flag": False,
                    "number": 0,
                    "revealed": False,
                    "id": 2,
                },
                {
                    "name": "good_board",
                    "pos_x": 1,
                    "pos_y": 0,
                    "bomb": False,
                    "flag": False,
                    "number": 0,
                    "revealed": False,
                    "id": 3,
                },
                {
                    "name": "good_board",
                    "pos_x": 1,
                    "pos_y": 1,
                    "bomb": False,
                    "flag": False,
                    "number": 0,
                    "revealed": False,
                    "id": 4,
                },
            ],
            "good_board_bad_squares": [
                {
                    "name": "good_board_bad_squares",
                    "pos_x": 0,
                    "pos_y": 0,
                    "bomb": False,
                    "flag": False,
                    "number": 0,
                    "revealed": False,
                    "id": 1,
                },
                {
                    "name": "good_board_bad_squares",
                    "pos_x": 0,
                    "pos_y": "dog",
                    "bomb": 999,
                    "flag": None,
                    "number": [],
                    "revealed": False,
                    "id": 2,
                },
                {
                    "name": "good_board_bad_squares",
                    "pos_x": 1,
                    "pos_y": 0,
                    "bomb": False,
                    "flag": False,
                    "number": 0,
                    "revealed": False,
                    "id": 3,
                },
                {
                    "name": "good_board_bad_squares",
                    "pos_x": 1,
                    "pos_y": 1,
                    "bomb": False,
                    "flag": False,
                    "number": 0,
                    "revealed": False,
                    "id": 4,
                },
            ],
        }

    @staticmethod
    def validate_item(item):
        if item not in PysweeperItemTypes.__dict__.values():
            raise TypeError(
                f"Expected a PysweeperItemType, but got ",
                f" value={item} type={type(item)}",
            )

    @staticmethod
    def validate_type(data, expected_type: type):
        if type(data) is not expected_type:
            raise TypeError(
                f"Data must be of type: dict " f"Given: value={data} type={type(data)}"
            )

    def connect(source):
        """connect to mock db"""

    def disconnect(source):
        """disconnect from mock db"""

    def create(self, item: str, data: dict):
        """Create a record in mock db"""
        self.validate_item(item)
        self.validate_type(data, dict)

    def read_many(self, item: PysweeperItemTypes, filter: dict):
        """Read many records from mock db"""
        self.validate_item(item)
        self.validate_type(filter, dict)

        name = filter.get("name")

        if item is PysweeperItemTypes.GAME:
            return self.board_records.get(name)
        elif item is PysweeperItemTypes.SQUARE:
            return self.square_records.get(name)
        else:
            raise ValueError(f"Unknown: {name}")

    def read_all(self, item: PysweeperItemTypes):
        """Read all items of a type in mock db"""
        self.validate_item(item)
        if item is PysweeperItemTypes.GAME:
            return self.board_records
        elif item is PysweeperItemTypes.SQUARE:
            return self.square_records
        else:
            raise TypeError(f"Unexpected PysweeperItemType")

    def read_one(self, item: str, filter: dict):
        """Read one record from mock db"""
        self.validate_item(item)
        self.validate_type(filter, dict)
        name = filter.get("name")
        return self.board_records.get(name)

    def update(self, item: PysweeperItemTypes, filter: dict, data: dict):
        """Update a record from mock db"""
        self.validate_item(item)
        self.validate_type(data, dict)
        self.validate_type(filter, dict)

    def destroy(self, item: PysweeperItemTypes, filter: dict):
        """Delete a record from mock db"""
        self.validate_item(item)
        self.validate_type(filter, dict)


class TestPysweeperSerializers(unittest.TestCase):

    def setUp(self):
        self.db = MockPysweeperDataConnector()
        self.serializer = PysweeperGameSerializer(self.db)

    def test_load_successful(self):
        """Test for successful load method execution"""
        game = self.serializer.load("good_board")
        self.assertIsInstance(game, GameBoard)

        for row in game.rows:
            for square in row:
                self.assertIsInstance(square, Square)

    def test_load_not_exist_failure(self):
        """Test for failure when passing a game name that doesn't exist"""
        with self.assertRaises(PysweeperGameDoesNotExist):
            self.serializer.load("i_dont_exist")

    def test_load_bad_name_type_failure(self):
        """Test for failure when passing in a bad name type"""
        with self.assertRaises(Exception):
            self.serializer.load(["not a string"])

    def test_load_no_game_found_failure(self):
        """Test for failure when passing in a name that doesn't exist"""
        with self.assertRaises(Exception):
            self.serializer.load({"name": "i_dont_exist"})

    def test_save_update_successful(self):
        """Test for successful save update method execution"""
        game = self.serializer.load("good_board")

        with self.assertLogs("pysweeper", level="DEBUG") as logs:
            self.serializer.save(game)

        self.assertTrue("Updating game" in logs.output[0])

    def test_save_create_successful(self):
        """Test for successful save create method execution"""
        game = GameBoard(name="new_game")
        game.buildBoard()
        with self.assertLogs("pysweeper", level="INFO") as logs:
            self.serializer.save(game)

        self.assertTrue("Saving new game" in logs.output[0])

    def test_delete_successful(self):
        with self.assertLogs("pysweeper", level="DEBUG") as logs:
            self.serializer.delete("good_board")

        self.assertTrue("Deleting game" in logs.output[0])

    def test_delete_not_exist_failure(self):
        """Test for failure when game does not exist"""
        with self.assertRaises(PysweeperGameDoesNotExist):
            self.serializer.delete("i_dont_exist")


if __name__ == "__main__":
    unittest.main()
