"""
Pysweeper Exceptions
"""

class PysweeperBadName(Exception):
    """Thrown when a bad name is passed by the user"""

class PysweeperBadCoords(Exception):
    """Thrown when a player sends coordinates outside of play area"""

class PysweeperBadDifficulty(Exception):
    """Thrown when a player an invalid difficulty is passed by the user"""

class PysweeperInvalidTimeDate(Exception):
    """Thrown when an invalid time or date is passed by the user"""

class PysweeperGameDoesNotExist(Exception):
    """Thrown when a player references a game that doesn't exist"""

class PysweeperGameAlreadyExists(Exception):
    """Thrown when a player passes a name that already exists"""