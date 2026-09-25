"""
The bridge between what comes in through the frontend
and what comes out of the backend.
"""

from abc import ABC, abstractmethod
from choices import PysweeperItemTypes
from data import PysweeperData
from exceptions import (PysweeperGameAlreadyExists,
                        PysweeperGameDoesNotExist,
                        PysweeperBadCoords)
from validators import (game_validator,
                        difficulty_validator,
                        elapsed_time_validator,
                        date_validator,
                        coords_validator)

class PysweeperSerializer(ABC):
    """The contract for all serializers"""
    def __init__(self, data_source: PysweeperData):
        self.data = data_source

    @abstractmethod
    def validate():
        """validate method"""

    @abstractmethod
    def save():
        """save method"""

#    @abstractmethod
#    def read():
#        """read method"""

class PysweeperGameSerializer(PysweeperSerializer):
    # define fields
    def __init__(self, data_source: PysweeperData):
        super().__init__(data_source)

    def validate(self, name: str, difficulty: int):
        """validate method"""
        game_validator(name)
        difficulty_validator(difficulty)
        # Make sure no game exists with name
        game = self.data.read(PysweeperItemTypes.GAME, name)
        if game:
            raise PysweeperGameAlreadyExists(f"Game already exists for: {name}")

    def save(self, name: str, difficulty: int):
        """save method"""
        self.data.create(PysweeperItemTypes.GAME, name, difficulty)

class PysweeperUpdateGameSerializer(PysweeperSerializer):
    # define fields
    def __init__(self, data_source: PysweeperData, name: str, square: tuple[int]):
        super().__init__(data_source)
        # TODO: create a game type
        # self.game = None
        # TODO: create a square type
        # self.square = None
        
        # Doing it this way would leave it to the data layer to raise for not found
        # this would also require that the views would need to catch the error
        # But doing it this way means that I could just use .save()
        self.game = self.data.read(PysweeperItemTypes.GAME, game_validator(name))
        self.square = self.data.read(PysweeperItemTypes.SQUARE, coords_validator(square))

    def validate(self, name: str, square: tuple[int]):
        """validate method"""
        game_validator(name)
        coords_validator(square)
        game = self.data.read(PysweeperItemTypes.GAME, name)
        selected = self.data.read(square)
        if not game:
            raise PysweeperGameDoesNotExist(f"Game does not exist: {name}")

        if not selected:
            raise PysweeperBadCoords(f"No square found for: {square}")

        self.game = game
        self.square = selected

    def save(self):
        """save method"""
        self.data.update(PysweeperItemTypes.SQUARE, self.square, clicked=True)


class PysweeperDeleteGameSerializer(PysweeperSerializer):
    # define fields
    def validate():
        """validate method"""

    def save():
        """save method"""

class PysweeperScoreboardSerializer(PysweeperSerializer):
    def validate():
        """validate method"""

    def save():
        """save method"""

    def read():
        """read method"""
