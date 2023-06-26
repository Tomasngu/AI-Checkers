"""Module to test checkers class"""

import pytest
from game.checkers import Checkers


@pytest.mark.parametrize("color, expected",
                         [(1, True),
                          (2, False),
                          (3, True),
                          (4, False)
                          ])
def test_on_turn(color, expected):
    """Test if piece is on turn"""
    game = Checkers(0)
    assert game.on_turn(color) == expected


def test_change_turn():
    """Test if two pieces are opponents"""
    game = Checkers(0)
    for i in range(10):
        if i % 2:
            assert game.on_turn(2)
        else:
            assert game.on_turn(1)
        game.change_turn()
