from backend.pysweeper import GameBoard, Square
from backend.data.models import GameRecordModel, SquareRecordModel


class SQLiteGameRecordModel(GameRecordModel):
    """Game Record Model"""

    DB_EXCLUDES = ["rows"]
    DB_INCLUDES = ["name", "difficulty", "game_over", "start_date", "end_date"]
    OBJ_EXCLUDES = ["game_over", "start_date", "end_date"]
    OBJ_INCLUDES = ["name", "difficulty"]

    def __init__(self, target: dict):
        """Game record"""
        self.target = target

    def db(self) -> dict:
        """
        From Obj -> To DB
        DB representation of record
        """
        payload = {}
        for inc in self.DB_INCLUDES:
            if inc in self.target.keys():
                payload[inc] = self.target[inc]
        return payload

    def obj(self) -> dict:
        """
        From DB -> To Obj
        Returns constructor args to
        satisfy requirements for GameBoard
        """
        payload = {}
        for inc in self.OBJ_INCLUDES:
            payload[inc] = self.target[inc]
        return payload


class SQLiteSquareRecordModel(SquareRecordModel):
    """Square Record Model"""

    DB_EXCLUDES = []
    OBJ_EXCLUDES = []

    def __init__(self, target: dict):
        """Square record"""
        self.target = target

    def db(self, name: str) -> dict:
        """DB representation of square record"""
        # TODO: name is required and cannot be None
        payload = self.target
        payload["name"] = name
        payload["bomb"] = int(payload["bomb"])
        payload["flag"] = int(payload["flag"])
        payload["revealed"] = int(payload["revealed"])
        return payload

    def obj(self) -> dict:
        """Attributes for building Square"""
        payload = self.target
        del payload["name"]
        del payload["id"]
        payload["bomb"] = bool(payload["bomb"])
        payload["flag"] = bool(payload["flag"])
        payload["revealed"] = bool(payload["revealed"])
        return payload
