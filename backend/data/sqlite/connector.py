from backend.data.sqlite.choices import PYSWEEPER_TABLE_COLUMN_CHOICES
from backend.data.connector import PysweeperDataConnector
from backend.data.exceptions import PysweeperDataConnectorError
from backend.data.sqlite.models import SQLiteGameRecordModel, SQLiteSquareRecordModel
from backend.data.sqlite.initializer import PysweeperSQLiteSeeder
from pathlib import Path
from contextlib import closing
import sqlite3
import logging

logger = logging.getLogger("pysweeper")


class PysweeperSQLiteData(PysweeperDataConnector):
    """Database Connector for sqlite"""

    GAME_MODEL = SQLiteGameRecordModel
    SQUARE_MODEL = SQLiteSquareRecordModel
    # TODO: put schema object (and table col choices) here
    # abstract out the schema so it's not "pysweeper specific"

    def __init__(self, address: str):
        """constructor"""
        self.path = Path(address)

        if not self.path.exists():
            logger.info(f"No DB found at {address}! Initializing...")
            init = PysweeperSQLiteSeeder(self.path)
            init.initialize()

        self.address = address

        # logger.info(f"Connecting to DB at: {self.address}")
        # self.db = sqlite3.connect(self.address)
        # self.cursor = self.db.cursor()

    # TODO: helper function to always swap bools to ints
    def _validator(self, item: str, target: dict) -> dict:
        """Validates incoming filter data"""
        if type(target) is not dict:
            raise TypeError(f"Data/Filter must be dict! Given: {type(target)}")

        allowed_columns = PYSWEEPER_TABLE_COLUMN_CHOICES[item]
        if not all([key in allowed_columns for key in target.keys()]):
            raise PysweeperDataConnectorError(
                f"Data/Filter contains invalid column! "
                f"Expected: {allowed_columns} Given: {target}"
            )

        # all bools must be ints when querying sqlite db
        for key, val in target.items():
            if type(val) == bool:
                target[key] = int(val)

        return target

    def create(self, item: str, data: dict):
        """A way to send changes to the source"""
        columns = self._validator(item, data)
        # logger.debug(f"Building insert statment for: {item}")
        inserts = tuple(data.values())
        questions = ", ".join("?" for _ in columns)
        query = f"INSERT INTO {item} ({", ".join(columns)}) VALUES({questions});"

        # logger.debug(f"Executing insert statement for: {item}")
        with closing(sqlite3.connect(self.address)) as connection:
            with connection:
                cursor = connection.cursor()
                cursor.execute(query, inserts)
                connection.commit()

    def read_many(self, item: str, filter: dict) -> list[dict]:
        """Get many items"""
        allowed_columns = PYSWEEPER_TABLE_COLUMN_CHOICES[item]
        vald_filter = self._validator(item, filter)
        filter_keys = list(vald_filter.keys())

        where_statements = "AND ".join([f"{key} = ? " for key in filter_keys])
        filter_values = tuple(val for val in vald_filter.values())
        query = f"SELECT * FROM {item} WHERE {where_statements}"

        # logger.debug(f"Querying: {vald_filter}")
        with closing(sqlite3.connect(self.address)) as connection:
            with connection:
                cursor = connection.cursor()
                cursor.execute(query, filter_values)
                rows = cursor.fetchall()

        if not rows:
            return None

        objects = []
        for row in rows:
            data = {}
            for index, dat in enumerate(row):
                data[allowed_columns[index]] = dat

            objects.append(data)

        return objects

    def read_all(self, item: str) -> list[dict]:
        """Get all items"""
        query = f"SELECT * FROM {item};"

        # logger.debug(f"Retrieving all of item: {item}")
        with closing(sqlite3.connect(self.address)) as connection:
            with connection:
                rows = self.cursor.execute(query)

        if not rows:
            return None

        objects = []
        for row in rows:
            data = {}
            for index, dat in enumerate(row):
                data[PYSWEEPER_TABLE_COLUMN_CHOICES[item][index]] = dat

            objects.append(data)

        return objects

    def read_one(self, item: str, filter: dict) -> dict:
        """Get ONLY one item"""
        allowed_columns = PYSWEEPER_TABLE_COLUMN_CHOICES[item]
        vald_filter = self._validator(item, filter)
        filter_keys = list(vald_filter.keys())

        where_statements = "AND ".join([f"{key} = ? " for key in filter_keys])
        filter_values = tuple(val for val in list(vald_filter.values()))
        query = f"SELECT * FROM {item} WHERE {where_statements}"

        # logger.debug(f"Queryring: {vald_filter}")
        with closing(sqlite3.connect(self.address)) as connection:
            with connection:
                cursor = connection.cursor()
                cursor.execute(query, filter_values)
                row = cursor.fetchone()

        if not row:
            return None

        data = {}
        for index, col in enumerate(row):
            data[allowed_columns[index]] = col

        return data

    def update(self, item: str, filter: dict, data: dict):
        """A way to update existing information"""
        vald_filter = self._validator(item, filter)
        vald_data = self._validator(item, data)

        filter_keys = list(vald_filter.keys())

        name = vald_filter.get("name")
        if not name:
            raise PysweeperDataConnectorError(
                f"Item name must be provided in filter! Given: {filter}"
            )

        columns = list(vald_data.keys())

        # logger.debug(f"{name}: Building update statment for: {item}")

        set_statements = ", ".join([f"{col} = ?" for col in columns])
        where_statements = "AND ".join([f"{key} = ? " for key in filter_keys])
        query = f"UPDATE {item} SET {set_statements} WHERE {where_statements}"

        filter_values = tuple(val for val in vald_filter.values())
        updates = tuple(list(data.values()))

        # logger.debug(f"{name}: Executing update statement for: {item}")
        with closing(sqlite3.connect(self.address)) as connection:
            with connection:
                cursor = connection.cursor()
                cursor.execute(query, updates + filter_values)
                connection.commit()

    def destroy(self, item: str, filter: dict):
        """A way to destroy existing data"""
        vald_filter = self._validator(item, filter)
        filter_keys = list(vald_filter.keys())

        where_statements = "AND ".join([f"{key} = ? " for key in filter_keys])
        delete = f"DELETE FROM {item} WHERE {where_statements}"

        filter_values = tuple(val for val in vald_filter.values())

        # logger.debug(f"Deleting item: {item} -> {vald_filter}")
        with closing(sqlite3.connect(self.address)) as connection:
            with connection:
                cursor = connection.cursor()
                cursor.execute(delete, filter_values)
                connection.commit()
