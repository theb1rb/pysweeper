# from abc import ABC, abstractmethod
from backend.exceptions import (
    PysweeperValueError,
    PysweeperValidationError,
    PysweeperBadName,
    PysweeperBadDifficulty,
    PysweeperInvalidTimeDate,
    PysweeperBadCoords,
)
from backend.settings import FORBIDDEN_CHARS, MAX_DIFFICULTY, MAX_GRID, MIN_GRID
from json import loads, JSONDecodeError
import logging

logger = logging.getLogger("pysweeper")


class PysweeperValidators:
    def __init__(self):
        self.validators = {
            "x": self.coords_validator,
            "y": self.coords_validator,
            "name": self.game_validator,
            "difficulty": self.difficulty_validator,
            "flag": self.bomb_flag_clicked_validator,
        }

    @staticmethod
    def json_loader(data: str) -> dict:
        """Verify JSON string"""
        # if type(data) is not str:
        #    raise PysweeperValidationError

        try:
            body = loads(data)
            return body
        except TypeError:
            message = f"Expected JSON string! Given: {type(data)}"
            raise PysweeperValidationError(message)
        except JSONDecodeError:
            message = f"Invalid JSON string"
            raise PysweeperValidationError(message)

    def is_valid(self, data: str) -> bool:
        try:
            self.json_loader(data)
            return True
        except:
            return False

    def validated(self, _data: str | dict) -> dict:
        if type(_data) == str:
            data: dict = self.json_loader(_data)
        else:
            data = _data

        for key, val in data.items():
            if key in self.validators.keys():
                self.validators[key](val)

        return data

    def game_validator(self, name: str):
        """Verify game name is acceptable"""
        if type(name) is not str:
            raise PysweeperBadName("Name must be a string! " f"Given: {type(name)}")

        if len(name) > 25:
            raise PysweeperBadName(
                "Name must be under 25 characters! " f"Given: {len(name)}"
            )

        bad_chars = [char for char in name if char in FORBIDDEN_CHARS]
        if len(bad_chars) > 0:
            # if characters in name are url unsafe, raise
            raise PysweeperBadName(
                "Name contains forbidden characters! " f"Bad Chars: {bad_chars}"
            )

    def difficulty_validator(self, difficulty: int):
        """Verify game difficulty is acceptable"""
        if type(difficulty) is not int:
            raise PysweeperBadDifficulty(
                "Difficulty must be an integer! " f"Given: {type(difficulty)}"
            )

        if not 0 <= difficulty < MAX_DIFFICULTY:
            raise PysweeperBadDifficulty(
                "Difficulty outside of range! "
                f"Expected: 0-{MAX_DIFFICULTY} Given: {difficulty}"
            )

    def coords_validator(self, *args):
        """Verify submitted coordinates are acceptable"""

        for coord in args:
            if type(coord) is not int:
                raise PysweeperBadCoords(
                    "Coordinates must be integers! " f"Given: {coord}"
                )

            if not 0 <= coord <= MAX_GRID:
                raise PysweeperBadCoords(
                    f"Coordinates must within range 0-{MAX_GRID}! " f"Given: {coord}"
                )

    def grid_size_validator(self, size: int):
        """Verify grid not too big or not too small"""
        if type(size) is not int:
            raise PysweeperValidationError(
                "Grid size must be an integer! " f"Given: {type(size)}"
            )

        if not MIN_GRID <= size <= MAX_GRID:
            raise PysweeperValidationError(
                f"Grid size must be between {MIN_GRID}-{MAX_GRID}! " f"Given: {size}"
            )

    def elapsed_time_validator(time: str):
        """Verify time submission is acceptable"""

    def date_validator(date: str):
        """Verify date submission is acceptable"""
        # may not need this one because the backend
        # might do all that work on it's own

    def bomb_flag_clicked_validator(self, item: bool):
        """Verify that bombs, flags, and clicked values are boolean"""
        if type(item) is not bool:
            raise PysweeperValidationError(
                "Bomb, flag, and clicked values must be boolean! "
                f"Given: {type(item)}"
            )
