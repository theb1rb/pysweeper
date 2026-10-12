class RecordModel:
    """
    Record Model Contract
    The idea is to add or subtract fields or
    columns that don't belong depending on
    whether an object is being made or unmade
    """

    def __init__(self, target: dict):
        """Build record model"""

    def db(self):
        """DB representation of record"""

    def obj(self) -> dict:
        """Attributes for building object"""


class GameRecordModel(RecordModel):
    """Game Record Model"""


class SquareRecordModel(RecordModel):
    """Square Record Model"""
