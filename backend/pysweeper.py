"""
Pysweeper Backend
"""

import random


class Square:
    def __init__(
        self,
        pos_x: int,
        pos_y: int,
        number: int = 0,
        bomb: bool = False,
        flag: bool = False,
        revealed: bool = False,
    ):
        self.pos_x: int = pos_x
        self.pos_y: int = pos_y
        self.number: int = number
        self.bomb: bool = bomb
        self.flag: bool = flag
        self.revealed: bool = revealed

    def getNeighbors(self, board):
        check_nums = [-1, 0, 1]
        for x in check_nums:
            for y in check_nums:
                if x == 0 and y == 0:
                    continue
                nx = self.pos_x + x
                ny = self.pos_y + y
                if (0 <= nx < board.grid_x) and (0 <= ny < board.grid_y):
                    yield (nx, ny)

    def calculateBombNumber(self, board: GameBoard):
        count = 0
        for neigh in self.getNeighbors(board):
            if board.getSquare(neigh[0], neigh[1]).bomb:
                count += 1
        self.number = count


class GameBoard:
    def __init__(self, name: str = "PySweeper", difficulty: int = 1):
        self.name: str = name
        self.difficulty: int = difficulty  # easy, medium, hard
        self.base: int = 15
        self.grid_x: int = self.base * self.difficulty
        self.grid_y: int = self.base * self.difficulty
        self.total_squares: int = self.grid_x * self.grid_y
        self.total_bombs: int = self.total_squares // 7
        # TODO: don't need to track this, just run pickBombs in build
        self.bomb_locations: set[tuple[int, int]] = self.pickBombLocations()
        # TODO: turn these into attribute methods
        self.revealed_squares: int = 0
        self.revealable_squares: int = self.total_squares - self.total_bombs
        # self.rows: list = [[None for _ in range(self.grid_x)] for _ in range(self.grid_y)]
        self.rows: list = []
        self.game_over: bool = False
        # self.buildBoard()

    def getSquare(self, pos_x, pos_y) -> Square | None:
        # try except for in case the coordinates are out of bounds
        if 0 <= pos_x < self.grid_x and 0 <= pos_y < self.grid_y:
            return self.rows[pos_x][pos_y]
        return None

    def getAllSquares(self) -> list[Square]:
        all_squares = []
        for row in self.rows:
            for square in row:
                all_squares.append(square)
        return all_squares

    def buildBoard(self):
        for x in range(self.grid_x):
            self.rows.append([])
            for y in range(self.grid_y):
                self.rows[x].append(
                    Square(pos_x=x, pos_y=y, bomb=((x, y) in self.bomb_locations))
                )

        for square in self.getAllSquares():
            if not square.bomb:
                square.calculateBombNumber(self)

    def pickBombLocations(self) -> set[tuple[int, int]]:
        bomb_indices = random.sample(range(self.total_squares), k=self.total_bombs)
        return {(i // self.grid_y, i % self.grid_y) for i in bomb_indices}

    def click(self, x: int, y: int):
        square = self.getSquare(x, y)
        if square and not square.revealed and not square.flag:
            return self.reveal(square)

    def revealZeros(self, square: Square):
        revealed = []
        for neigh in square.getNeighbors(self):
            next_square = self.getSquare(neigh[0], neigh[1])
            if not next_square or next_square.revealed or next_square.bomb:
                continue

            next_square.revealed = True
            revealed.append(next_square)
            self.revealed_squares += 1
            if next_square.number == 0:
                revealed.extend(self.revealZeros(next_square))
            # self.reveal(next_square)
        # TODO: add tests for the list this returns
        return revealed

    def reveal(self, square: Square) -> list[Square]:
        # TODO: this now returns a list. Should add tests for it
        if not square.flag:

            self.revealed_squares += 1
            square.revealed = True

            if square.bomb:
                self.game_over = True
                return self.getAllSquares()

            revealed = [square]

            if square.number == 0:
                revealed += self.revealZeros(square)

            if self.revealed_squares >= self.revealable_squares:
                self.game_over = True

            return revealed


class Scoreboard:
    """Pysweeper Scoreboard"""


#    def __init__(self, name: str = "pysweeper-scoreboard"):
#        self.scoreboard_base_path: str = ""
#        self.name: str = f"{name}.txt"
#        self.best: int = 999


# Counter Model - counts flags, bomb left, and adjacent bombs

# StopWatch - time passed after game start -> put on scoreboard
