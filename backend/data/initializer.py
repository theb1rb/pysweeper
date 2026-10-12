from abc import ABC, abstractmethod
from backend.data.connector import PysweeperDataConnector


class PysweeperDataManager(ABC):
    """
    Mechanism for intializing bare databases
    in order to run Pysweeper
    """

    def __init__(self, db: PysweeperDataConnector):
        """Constructor"""

    @abstractmethod
    def initialize(self):
        """Begin intialization of DB"""

    @abstractmethod
    def delete(self):
        """Delete DB Tables"""
