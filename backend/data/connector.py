"""
Pysweeper's data layer:
This should include the lower level details of
communicating with things like databases
"""

from abc import ABC, abstractmethod
from backend.data.models import GameRecordModel, SquareRecordModel

# from choices import PysweeperItemTypes


class PysweeperDataConnector(ABC):
    """All data classes will follow this contract"""

    GAME_MODEL = GameRecordModel
    SQUARE_MODEL = SquareRecordModel

    def __init__(self, address):
        """Connect to DB and be ready to operate"""

    @abstractmethod
    def create(self, item: str, data: dict):
        """A way to send changes to the source"""

    @abstractmethod
    def read_many(self, item: str, filter: dict):
        """Get many items"""

    @abstractmethod
    def read_all(self, item: str):
        """Get all items"""

    @abstractmethod
    def read_one(self, item, filter: dict):
        """Get ONLY one item"""

    @abstractmethod
    def update(self, item: str, filter: dict, data: dict):
        """A way to update existing information"""

    @abstractmethod
    def destroy(self, item: str, filter: dict):
        """A way to destroy existing data"""
