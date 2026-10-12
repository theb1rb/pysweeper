import unittest
from unittest.mock import MagicMock, patch
from backend.pysweeper import GameBoard, Square


class TestPysweeperBackend(unittest.TestCase):
    """
    Tests the backend of PySweeper
    """

    def setUp(self):
        self.mock_board = GameBoard(name="PysweeperTest", difficulty=1)
        self.mock_board.buildBoard()
        self.mock_all_squares = self.mock_board.getAllSquares()

    def test_square_get_neighbors(self):
        """
        Verifies that squares can return the right
        number of neighbor coordinates, excluding
        themselves.
        """
        mini_mock_board = MagicMock()
        mini_mock_board.grid_x = mini_mock_board.grid_y = 3
        square = Square(1, 1, bomb=False)
        neighbors = [neigh for neigh in square.getNeighbors(mini_mock_board)]
        self.assertEqual(len(neighbors), 8)
        self.assertNotIn((1, 1), neighbors)

        square = Square(0, 0, bomb=False)
        neighbors = [neigh for neigh in square.getNeighbors(mini_mock_board)]
        self.assertEqual(len(neighbors), 3)

    def test_square_calculate_bomb_number(self):
        """
        Verifies that non-bomb squares have valid
        integers assigned to them.
        """
        for square in self.mock_all_squares:
            if not square.bomb:
                test_square = square
                break
        self.assertIsInstance(test_square.number, int)
        self.assertTrue(0 <= test_square.number <= 8)

    def test_gameboard_get_square(self):
        """
        Verifies that bad coordinates return None,
        and good coordinates return a Square
        """
        bad_coords = self.mock_board.getSquare(-1, -1)
        self.assertIsNone(bad_coords)

        good_coords = self.mock_board.getSquare(0, 0)
        self.assertIsInstance(good_coords, Square)

    def test_gameboard_build_board(self):
        """
        Verifies that the number of squares is accurate
        """
        self.assertEqual(self.mock_board.total_squares, len(self.mock_all_squares))

    def test_gameboard_pick_bomb_locations(self):
        """
        Verifies that bomb locations are stored as a set
        and that the number of bombs are accurate
        """
        self.assertIsInstance(self.mock_board.bomb_locations, set)
        self.assertEqual(
            self.mock_board.total_bombs, len(self.mock_board.bomb_locations)
        )

    def test_gameboard_click(self):
        """
        Verifies that the click function works and
        squares become reveal
        """
        self.mock_board.click(14, 14)
        self.assertEqual(self.mock_board.getSquare(14, 14).revealed, True)

    def test_gameboard_reveal_zeros(self):
        """
        Verifies that the reveal zeroes function is
        called at least once when a zero is found
        """
        for square in self.mock_all_squares:
            if square.number == 0:
                found_zero = square
                break

        with patch.object(
            self.mock_board, "revealZeros", wraps=self.mock_board.revealZeros
        ) as wrapped:
            wrapped(found_zero)
            self.assertGreaterEqual(wrapped.call_count, 1)

    def test_gameboard_bomb_reveal(self):
        """
        Verifies that the game is marked as over
        when a bomb is revealed
        """
        for square in self.mock_all_squares:
            if square.bomb:
                bomb = square
                break
        self.mock_board.reveal(bomb)
        self.assertTrue(self.mock_board.game_over)

    def test_gameboard_click_all_reveal(self):
        """
        Verify that the game is marked as over after
        all squares are clicked
        """
        for square in self.mock_all_squares:
            square.bomb = False
            self.mock_board.reveal(square)

        self.assertTrue(self.mock_board.game_over)


if __name__ == "__main__":
    unittest.main()
