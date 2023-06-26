"""Module for testing board methods"""

import pytest
from game.board import Board
import numpy as np


@pytest.mark.parametrize("size", [10, 8, 6, 4])
def test_init(size):
    """Test board init"""
    board = Board(size, size, 0, 0)
    assert board.grid.shape[0] == size
    assert board.white_count == board.black_count
    assert board.white_count == size*(size - 2)/4
    assert board.winner is None


@pytest.mark.parametrize("row, col, expected", [(3, 4, True),
                                                (0, 0, True),
                                                (-1, 0, False),
                                                (3, 8, False)])
def test_valid_square(row, col, expected) -> bool:
    """Check if (row, col) is a valid square on board"""
    board = Board(8, 8, 0, 0)
    assert board.valid_square(row, col) == expected


@pytest.mark.parametrize("row, col, new_row, new_col",
                         [(1, 4, 5, 4),
                          (1, 4, 7, 4),
                             (1, 0, 5, 4),
                             (0, 3, 2, 3)])
def test_apply_move(row, col, new_row, new_col):
    """Test apply move"""
    board = Board(8, 8, 0, 0)
    board.apply_move(row, col, new_row, new_col, [])
    assert board.grid[row, col] == 0
    assert board.grid[new_row, new_col] != 0


@pytest.mark.parametrize("row, col, expected",
                         [(3, 4, 0),
                          (0, 1, 2),
                             (2, 3, 2),
                             (7, 0, 1)])
def test_get_piece(row, col, expected):
    """Test retrieving pieces"""
    board = Board(8, 8, 0, 0)
    assert board.get_piece(row, col) == expected


@pytest.mark.parametrize("captured_pieces",
                         [[(3, 4), (1, 2)],
                          [(0, 1), (0, 3), (0, 5), (0, 7)],
                          [(7, 1), (7, 3), (7, 5), (7, 7)]])
def test_remove_captured(captured_pieces):
    """Test remove captured pieces from board"""
    board = Board(8, 8, 0, 0)
    board.remove_captured(captured_pieces)
    for piece in captured_pieces:
        assert board.grid[*piece] == 0


@pytest.mark.parametrize("color, expected",
                         [(1, [(-1, 1), (-1, -1)]),
                          (2, [(1, 1), (1, -1)]),
                          (3, [(-1, 1), (-1, -1), (1, 1), (1, -1),]),
                          (4, [(-1, 1), (-1, -1), (1, 1), (1, -1),])
                          ])
def test_get_dirs(color, expected):
    """Test get dirs for given piece color"""
    board = Board(8, 8, 0, 0)
    assert board.get_dirs(color) == expected


@pytest.mark.parametrize("piece, other, expected",
                         [(1, 1, False),
                          (2, 1, True),
                          (1, 3, False),
                          (1, 4, True),
                          (2, 3, True)
                          ])
def test_is_opponent(piece, other, expected):
    """Test if two pieces are opponents"""
    board = Board(8, 8, 0, 0)
    assert board.is_opponent(piece, other) == expected


GRID1 = np.array([[0, 2, 0, 2, 0, 2, 0, 2],
                  [2, 0, 2, 0, 2, 0, 2, 0],
                  [0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0]], dtype=int)
GRID2 = np.array([[0, 2, 0, 2, 0, 2, 0, 2],
                  [2, 0, 0, 0, 2, 0, 0, 0],
                  [0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 2, 0, 0, 0, 0],
                  [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]], dtype=int)
GRID3 = np.array([[0, 2, 0, 2, 0, 2, 0, 2],
                  [2, 0, 0, 0, 2, 0, 0, 0],
                  [0, 2, 0, 2, 0, 2, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 2, 0, 0, 0, 0],
                  [1, 0, 3, 0, 1, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]], dtype=int)


@pytest.mark.parametrize("grid, row, col, piece_type, expected",
                         [(GRID1, 5, 2, 1, [((4, 3), []), ((4, 1), [])]),
                          (GRID1, 2, 1, 2, [((3, 2), []), ((3, 0), [])]),
                          (GRID2, 5, 2, 1, [
                           ((1, 6), [(4, 3), (2, 5)]), ((1, 2), [(4, 3), (2, 3)])]),
                          (GRID3, 5, 2, 3, [
                           ((3, 0), [(4, 3), (2, 3), (2, 1)])])
                          ])
def test_get_valid_moves(grid, row, col, piece_type, expected):
    """Test valid moves for given piece"""
    board = Board(8, 8, 0, 0)
    board.grid = grid
    assert board.get_valid_moves(row, col, piece_type) == expected


@pytest.mark.parametrize("grid, color,  expected",
                         [(GRID1, 1, {(5, 0): [((4, 1), [])],
                                      (5, 2): [((4, 3), []), ((4, 1), [])],
                                      (5, 4): [((4, 5), []), ((4, 3), [])],
                                      (5, 6): [((4, 7), []), ((4, 5), [])]}),
                          (GRID2, 1, {
                           (5, 2): [((1, 6), [(4, 3), (2, 5)]), ((1, 2), [(4, 3), (2, 3)])]}),
                          (GRID3, 1, {
                           (5, 2): [((3, 0), [(4, 3), (2, 3), (2, 1)])]}),
                          (GRID3, 2, {
                           (4, 3): [((6, 5), [(5, 4)]), ((6, 1), [(5, 2)])]})
                          ])
def test_get_valid_moves_all_pieces(grid, color, expected):
    """Test get valid moves for all pieces of given color"""
    board = Board(8, 8, 0, 0)
    board.grid = grid
    assert board.get_valid_moves_all_pieces(color) == expected
