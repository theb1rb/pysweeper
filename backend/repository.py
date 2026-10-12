from abc import ABC, abstractmethod
from backend.data.connector import PysweeperDataConnector
from backend.serializers import PysweeperSerializer
from backend.pysweeper import GameBoard, Square
from backend.choices import PysweeperItemTypes


class Repository(ABC):
    """Repository contract"""

    def __init__(self, db: PysweeperDataConnector, serializer: PysweeperSerializer):
        """Constructor"""

    @abstractmethod
    def get(self):
        """Get something from the repository"""

    @abstractmethod
    def save(self):
        """Save something in the repository"""


class GameRepository(Repository):
    """GameRepository"""

    def __init__(self, db: PysweeperDataConnector, serializer: PysweeperSerializer):
        """Constructor"""
        self.db = db
        self.serializer = serializer

    def get(self, name: str) -> GameBoard:
        """Get a game"""
        if type(name) is not str:
            raise TypeError(f"Expected a string, but got {type(name)}")

    def save(self):
        """Save a game"""


class SquareRepository(Repository):
    """SquareRepository"""

    def __init__(self, db: PysweeperDataConnector, serializer: PysweeperSerializer):
        """Constructor"""
        self.db = db
        self.serializer = serializer

    def get(self):
        """Get a square"""

    def save(self):
        """Save a square"""

    def get_many(self):
        """Get many squares"""

    def save_many(self):
        """Save many squares"""
