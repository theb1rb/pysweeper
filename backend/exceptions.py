"""
Pysweeper Exceptions
"""


class PysweeperValueError(ValueError):
    """Pysweeper related value error"""


class PysweeperValidationError(Exception):
    """Pysweeper data validation Exception"""


class PysweeperBadName(PysweeperValidationError):
    """Thrown when a bad name is passed by the user"""


class PysweeperBadCoords(PysweeperValidationError):
    """Thrown when a player sends coordinates outside of play area"""


class PysweeperBadDifficulty(PysweeperValidationError):
    """Thrown when a player an invalid difficulty is passed by the user"""


class PysweeperInvalidTimeDate(PysweeperValidationError):
    """Thrown when an invalid time or date is passed by the user"""


class PysweeperGameDoesNotExist(PysweeperValueError):
    """Thrown when a player references a game that doesn't exist"""


class PysweeperGameAlreadyExists(PysweeperValueError):
    """Thrown when a player passes a name that already exists"""
