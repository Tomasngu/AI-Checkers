"""Module for testing AI methods"""
import pytest
from game.ai import AI
from game.board import Board
from tests.test_board import GRID1, GRID2, GRID3


@pytest.mark.parametrize("grid, expected",
                         [(GRID1, 0),
                          (GRID2, -70),
                          (GRID3, -65)
                          ])
def test_evaluate_board(grid, expected):
    """Test board first evaluation"""
    board = Board(8, 8, 0, 0)
    board.grid = grid
    epic_ai = AI(1)
    assert epic_ai.evaluate_board(grid) == expected

@pytest.mark.parametrize("grid, expected",
                         [(GRID1, 0),
                          (GRID2, -88),
                          (GRID3, -87)
                          ])
def test_evaluate_board2(grid, expected):
    """Test second board eval"""
    board = Board(8, 8, 0, 0)
    board.grid = grid
    epic_ai = AI(1)
    assert epic_ai.evaluate_board2(grid) == expected
    