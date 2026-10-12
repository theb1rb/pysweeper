from backend.exceptions import (
    PysweeperValueError,
    PysweeperValidationError,
    PysweeperBadName,
    PysweeperBadDifficulty,
    PysweeperInvalidTimeDate,
    PysweeperBadCoords,
)
import logging
from backend.settings import MAX_DIFFICULTY, MAX_GRID, MIN_GRID
import unittest
from unittest.mock import MagicMock, patch
from backend.validators import PysweeperValidators

logger = logging.getLogger("pysweeper")


class TestPysweeperValidators(unittest.TestCase):

    def setUp(self):
        self.valid_json = (
            '{"x": 1, "y": 2, "name": "Pysweeper", "difficulty": 1, "flag": false }'
        )

    def test_json_loader_success(self):
        """Verify that json returns a dict"""
        data = PysweeperValidators().json_loader(self.valid_json)
        self.assertIsInstance(data, dict)

    def test_json_loader_not_string_failure(self):
        """Verify failure when not passed a string"""
        with self.assertRaises(PysweeperValidationError):
            PysweeperValidators().json_loader(123)

    def test_json_loader_bad_json_string_failure(self):
        """Verify failure when json string is invalid"""
        with self.assertRaises(PysweeperValidationError):
            PysweeperValidators().json_loader("not a valid json")

    def test_is_valid_json_success(self):
        """Verifies success when valid json"""
        data = PysweeperValidators().is_valid(self.valid_json)
        self.assertTrue(data)

    def test_is_valid_fail(self):
        """Verifies false when not a valid json"""
        data = PysweeperValidators().is_valid("not a valid json")
        self.assertFalse(data)

    def test_validated_success(self):
        """Verify succes when validators return a data dict"""
        data = PysweeperValidators().validated(self.valid_json)
        self.assertIsInstance(data, dict)

    def test_validated_fails(self):
        """Verify failure when not passed a valid json"""
        with self.assertRaises(Exception):
            PysweeperValidators().validated("not a valid json")

    def test_game_validator_success(self):
        """Verify success when passed a valid game name"""
        PysweeperValidators().game_validator("Pysweeper")

    def test_game_validator_not_string_failure(self):
        """Verify failure when not passed a string"""
        with self.assertRaises(PysweeperBadName):
            PysweeperValidators().game_validator(123)

    def test_game_validator_too_long_failure(self):
        """Verify failure when game name too long"""
        with self.assertRaises(PysweeperBadName):
            PysweeperValidators().game_validator("abcdefghijklmnopqrstuvwxyz")

    def test_game_validator_bad_chars_failure(self):
        """Verify failure when passed forbidden chars"""
        with self.assertRaises(PysweeperBadName):
            PysweeperValidators().game_validator("@$<>?/\\{}[]~`| ")

    def test_difficulty_validator_success(self):
        """Verify success when passed valid difficulty"""
        PysweeperValidators().difficulty_validator(1)

    def test_difficulty_validator_not_int_failure(self):
        """Verify failure when not passed int"""
        with self.assertRaises(PysweeperBadDifficulty):
            PysweeperValidators().difficulty_validator("not an int")

    def test_difficulty_validators_too_big_failure(self):
        """Verify failure when passed a difficulty too big"""
        with self.assertRaises(PysweeperBadDifficulty):
            PysweeperValidators().difficulty_validator(MAX_DIFFICULTY + 1)

    def test_difficulty_validators_too_small_failure(self):
        """Verify failure when passed a difficulty too small"""
        with self.assertRaises(PysweeperBadDifficulty):
            PysweeperValidators().difficulty_validator(-1)

    def test_coords_validator_single_success(self):
        """Verify success when passed valid coords"""
        PysweeperValidators().coords_validator(0)

    def test_coords_validator_multiple_success(self):
        """Verify success when passed multiple valid coords"""
        PysweeperValidators().coords_validator(0, 1)

    def test_coords_validator_not_int_failure(self):
        """Verify failure when not passed an int"""
        with self.assertRaises(PysweeperBadCoords):
            PysweeperValidators().coords_validator("not an int")

    def test_coords_validator_too_big_failure(self):
        """Verify failure when passed a coordinate too big"""
        with self.assertRaises(PysweeperBadCoords):
            PysweeperValidators().coords_validator(MAX_GRID + 1)

    def test_coords_validators_too_small_failure(self):
        """Verify failure when passed a coordinate too small"""
        with self.assertRaises(PysweeperBadCoords):
            PysweeperValidators().coords_validator(-1)

    def test_grid_validator_success(self):
        """Verify success when passed valid grid size"""
        PysweeperValidators().grid_size_validator(15)

    def test_grid_validator_not_int_failure(self):
        """Verify failure when not passed an int"""
        with self.assertRaises(PysweeperValidationError):
            PysweeperValidators().grid_size_validator("not an int")

    def test_grid_validator_too_big_failure(self):
        """Verify failure when grid too big"""
        with self.assertRaises(PysweeperValidationError):
            PysweeperValidators().grid_size_validator(MAX_GRID + 1)

    def test_grid_validator_too_small_failure(self):
        """Verify failure when grid too small"""
        with self.assertRaises(PysweeperValidationError):
            PysweeperValidators().grid_size_validator(MIN_GRID - 1)

    def test_bomb_flag_clicked_validator_success(self):
        """Verify success when passed bool"""
        PysweeperValidators().bomb_flag_clicked_validator(True)

    def test_bomb_flag_clicked_not_bool_failure(self):
        """Verify failure when not passed bool"""
        with self.assertRaises(PysweeperValidationError):
            PysweeperValidators().bomb_flag_clicked_validator("not a bool")
