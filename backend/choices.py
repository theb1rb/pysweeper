from dataclasses import dataclass


@dataclass
class GameActionChoices:
    DELETE = "delete"
    NEW = "new"


@dataclass
class PysweeperItemTypes:
    SQUARE = "square"
    GAME = "game"
    PLAYER = "player"
    DIFFICULTY = "difficulty"
    TIME = "time"
    DATE = "date"


@dataclass
class PysweeperGameStatusChoices:
    PLAYING = "playing"
    OVER = "over"
