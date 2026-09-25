"""
Pysweeper's data layer:
This should include the lower level details of
communicating with things like databases
"""

from abc import ABC, abstractmethod
from choices import PysweeperItemTypes

class PysweeperData(ABC):
    """All data classes will follow this contract"""

    @abstractmethod
    def connect(source):
        """A way to connect to a source"""

    @abstractmethod
    def disconnect(source):
        """A way to disconnect from a source"""

    @abstractmethod
    def create(item, data):
        """A way to send changes to the source"""

    @abstractmethod
    def read(item, name):
        """A way to query and read data"""

    @abstractmethod
    def update(item, name, data):
        """A way to update existing information"""

    @abstractmethod
    def destroy(item, name):
        """A way to destroy existing data"""

class PysweeperSQLiteData(PysweeperData):
    pass