from backend.choices import PysweeperItemTypes
from backend.data.sqlite.choices import PYSWEEPER_TABLE_COLUMN_CHOICES
from backend.data.models import RecordModel, GameRecordModel, SquareRecordModel
from backend.data.sqlite.models import SQLiteSquareRecordModel, SQLiteGameRecordModel
from backend.pysweeper import GameBoard, Square
import unittest
from unittest.mock import MagicMock, patch


class TestSQLiteGameRecordModel(unittest.TestCase):
    """
    Test SQLiteGameRecordModel
    """

    def setUp(self):
        """setup test"""

    def test_db_success(self):
        """
        Test db() method to make sure it returns a dictionary.
        Test that dictionary has all the right key value pairs.
        """
        game = GameBoard(name="Pysweeper", difficulty=1)
        # game.buildBoard()

        game_attrs = game.__dict__
        # simulate a new game:
        game_attrs["start_date"] = "2026-10-02 12:00pm"
        game_attrs["end_date"] = None

        game_model = SQLiteGameRecordModel(game_attrs)
        game_record = game_model.db()

        self.assertIsInstance(game_record, dict)
        self.assertEqual(game_model.DB_INCLUDES, list(game_record.keys()))

    def test_obj_success(self):
        """
        Test obj() method to make sure it returns a dictionary.
        Test that dictionary has all the right key value pairs.
        """
        row = {
            "name": "Pysweeper",
            "difficulty": 1,
            "game_over": False,
            "start_date": "2026-10-02 12:00pm",
            "end_date": None,
        }

        game_model = SQLiteGameRecordModel(row)
        game_obj_args = game_model.obj()

        self.assertTrue(
            not any(item in game_model.OBJ_EXCLUDES for item in game_obj_args.keys())
        )

        board = GameBoard(**game_obj_args)
        self.assertIsInstance(board, GameBoard)


class TestSQLiteSquareModel(unittest.TestCase):
    """
    Test SQLiteSquareModel
    """

    def setUp(self):
        """Setup test"""

    def test_db_success(self):
        """
        Test db() method to make sure it returns a dictionary.
        Test that dictionary has all the right key value pairs.
        """
        square = Square(
            pos_x=0, pos_y=0, bomb=False, flag=False, number=0, revealed=False
        )

        square_model = SQLiteSquareRecordModel(square.__dict__)
        square_record = square_model.db(name="Pysweeper")

        self.assertIsInstance(square_record, dict)
        self.assertTrue(
            all(
                [
                    item in PYSWEEPER_TABLE_COLUMN_CHOICES[PysweeperItemTypes.SQUARE]
                    for item in list(square_record.keys())
                ]
            )
        )
        self.assertTrue(
            all(
                [
                    type(item) == int
                    for item in [
                        square_record["bomb"],
                        square_record["flag"],
                        square_record["revealed"],
                    ]
                ]
            )
        )

    def test_obj_success(self):
        """
        Test obj() method to make sure it returns a dictionary.
        Test that dictionary has all the right key value pairs.
        """
        square_row = {
            "name": "Pysweeper",
            "pos_x": 0,
            "pos_y": 0,
            "number": 0,
            "bomb": 0,
            "flag": 0,
            "revealed": 0,
            "id": 1,
        }
        square_model = SQLiteSquareRecordModel(square_row)
        square_obj = square_model.obj()

        self.assertIsInstance(square_obj, dict)
        self.assertTrue(
            all(
                [
                    item in PYSWEEPER_TABLE_COLUMN_CHOICES[PysweeperItemTypes.SQUARE]
                    for item in list(square_obj.keys())
                ]
            )
        )
        self.assertTrue(
            all(
                [
                    type(item) == bool
                    for item in [
                        square_obj["bomb"],
                        square_obj["flag"],
                        square_obj["revealed"],
                    ]
                ]
            )
        )
