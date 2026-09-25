# from abc import ABC, abstractmethod
from exceptions import (PysweeperBadName,
                        PysweeperBadDifficulty,
                        PysweeperInvalidTimeDate,
                        PysweeperBadCoords)
from settings import (FORBIDDEN_CHARS, 
                      MAX_DIFFICULTY,
                      MAX_GRID)

def game_validator(name: str):
    """Verify game name is acceptable"""
    if len(name) > 25:
        raise PysweeperBadName("Name must be under 25 characters! "
                                f"Given: {len(name)}")

    bad_chars = [char for char in name if char in FORBIDDEN_CHARS]
    if len(bad_chars) > 0:
        # if characters in name are url unsafe, raise
        raise PysweeperBadName("Name contains forbidden characters! "
                               f"Bad Chars: {bad_chars}")

def difficulty_validator(difficulty: int):
    """Verify game difficulty is acceptable"""
    if type(difficulty) is not int:
        raise PysweeperBadDifficulty("Difficulty must be an integer! "
                                     f"Given: {type(difficulty)}")

    if 0 <= difficulty < MAX_DIFFICULTY:
        raise PysweeperBadDifficulty("Difficulty outside of range! "
                                     f"Expected: 0-{MAX_DIFFICULTY} Given: {difficulty}")

def coords_validator(coords: tuple[int]):
    """Verify submitted coordinates are acceptable"""
    if type(coords) is not tuple:
        raise PysweeperBadCoords("Coordinates must be a tuple! "
                                 f"Given: {type(coords)}")

    if len(coords) != 2:
        raise PysweeperBadCoords("Coords must be provided as (x, y)! "
                                 f"Given: {coords}")

    if type(coords[0]) is not int or type(coords[1] is not int):
        raise PysweeperBadCoords("Coords must be a tuple of integers! "
                                 f"Given: {coords}")

    if coords[0] < 0 or coords[1] < 0:
        raise PysweeperBadCoords("Coords must be positive integers! "
                                 f"Given: {coords}")

    if coords[0] > MAX_GRID or coords[1] > MAX_GRID:
        raise PysweeperBadCoords(f"Coords must be below maximum grid size ({MAX_GRID})! "
                                 f"Given: {coords}")

def elapsed_time_validator(time: str):
    """Verify time submission is acceptable"""
    pass

def date_validator(date: str):
    """Verify date submission is acceptable"""
    # may not need this one because the backend
    # might do all that work on it's own
    pass
