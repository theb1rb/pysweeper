from backend.choices import PysweeperItemTypes
from backend.data.initializer import PysweeperDataManager
import logging
import sqlite3
from contextlib import closing

logger = logging.getLogger("pysweeper")


class PysweeperSQLiteSeeder(PysweeperDataManager):
    """Pysweeper sqlite intializer"""

    game_table = f"""CREATE TABLE IF NOT EXISTS {PysweeperItemTypes.GAME}(
                            name TEXT PRIMARY KEY NOT NULL,
                            difficulty INTEGER,
                            game_over INTEGER DEFAULT 0,
                            start_date TEXT DEFAULT NULL,
                            end_date TEXT DEFAULT NULL
                        )"""

    square_table = f"""CREATE TABLE IF NOT EXISTS {PysweeperItemTypes.SQUARE}(
                            name TEXT NOT NULL,
                            pos_x INTEGER,
                            pos_y INTEGER,
                            number INTEGER,
                            bomb INTEGER,
                            flag INTEGER,
                            revealed INTEGER,
                            id INTEGER PRIMARY KEY
                        )"""

    def __init__(self, address: str):
        self.path = address

    def initialize(self):
        """Intialize sqlite DB"""
        logger.info("Seeding SQLite DB Game and Square Tables")
        with closing(sqlite3.connect(self.path)) as connection:
            with connection:
                # TODO: figure out if I can do this with just one commit
                cursor = connection.cursor()
                cursor.execute(self.game_table)
                connection.commit()
                cursor.execute(self.square_table)
                connection.commit()

    def delete(self):
        """delete sqlite db tables"""
        with closing(sqlite3.connect(self.path)) as connection:
            with connection:
                cursor = connection.cursor()
                cursor.execute(f"DROP TABLE IF EXISTS {PysweeperItemTypes.GAME}")
                connection.commit()
                cursor.execute(f"DROP TABLE IF EXISTS {PysweeperItemTypes.SQUARE}")
                connection.commit()
