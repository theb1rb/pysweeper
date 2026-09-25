from abc import ABC, abstractmethod
from data import PysweeperData 

class PysweeperRepository(ABC):
    def __init__(self, data: PysweeperData):
        """Pysweeper repository"""
        self.data = data

    def get(*args, **kwargs):
        """Retrieve an object"""

class GameRepository(PysweeperRepository):
    def __init__(self, data: PysweeperData):
        super().__init__(data)
        self.games = None

    def _games():
        pass

    def get(*args, **kwargs):
        pass

class SquareRepository(PysweeperRepository):
    def __init__(self, data: PysweeperData, game):
        super().__init__(data)
        self.game = game
        self.squares = None

    def _squares() -> list:
        pass

    def get(*args, **kwargs):
        pass