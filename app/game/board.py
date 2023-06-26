"""Module for fast computing"""
from copy import deepcopy
import pygame
import numpy as np
from game.config import Colors
from game.config import StoneEnum
from game.config import StoneImages
from game.config import SizeConstants as const


class Board:
    """Class representing game board of checkers"""

    def __init__(self, rows: int, cols: int, cell_width: int, radius: int) -> None:
        self.rows = rows
        self.cols = cols

        self.white_count = 0
        self.black_count = 0
        self.winner = None

        # self.grid = np.zeros((rows, cols))
        self.grid = np.zeros((rows, cols), dtype=np.int8)
        self.cell_width = cell_width
        self.circle_radius = radius
        self.init_pieces()

        self.square = None
        self.previous_square = None

    def init_pieces(self) -> None:
        """Init pieces on the board"""
        game_rows = (self.rows - 2)//2
        # init black
        for row in range(game_rows):
            for col in range(self.cols):
                if (row + col) % 2 == 1:
                    self.grid[row, col] = StoneEnum.BLACK.value
                    self.black_count += 1
        for row in range(self.rows - game_rows, self.rows):
            for col in range(self.cols):
                if (row + col) % 2 == 1:
                    self.grid[row, col] = StoneEnum.WHITE.value
                    self.white_count += 1

    def draw_piece(self, screen, row, col, color) -> None:
        if color == StoneEnum.WHITE.value:
            img = StoneImages.WHITE_STONE
        elif color == StoneEnum.WHITE_KING.value:
            img = StoneImages.WHITE_KING
        elif color == StoneEnum.BLACK.value:
            img = StoneImages.BLACK_STONE
        else:
            img = StoneImages.BLACK_KING

        x_pos = col*self.cell_width
        y_pos = row*self.cell_width
        x_stone = x_pos + const.STONE_OFFSET
        y_stone = y_pos + const.STONE_OFFSET
        screen.blit(img, (x_stone, y_stone))

    def highlight_prev(self, screen):
        if self.square is not None:
            pygame.draw.rect(screen, Colors.YELLOW, (self.square[1]*self.cell_width, self.square[0]*self.cell_width,
                                                     self.cell_width, self.cell_width))
            pygame.draw.rect(screen, Colors.YELLOW, (self.previous_square[1]*self.cell_width, self.previous_square[0]*self.cell_width,
                                                     self.cell_width, self.cell_width))

    def highlight(self, screen, row: int, col: int):
        pygame.draw.rect(screen, Colors.YELLOW, (col*self.cell_width,
                         row*self.cell_width, self.cell_width, self.cell_width))

    def draw_pieces(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != 0:
                    self.draw_piece(screen, row, col, self.grid[row, col])

    def draw_all(self, screen) -> None:
        """Draws everything needed on screen"""
        self.draw_grid(screen)
        self.highlight_prev(screen)

    def draw_valid_moves(self, screen, valid_moves):
        for move, _ in valid_moves:
            row, col = move
            pygame.draw.circle(screen, Colors.BLUE, (col * self.cell_width + self.cell_width //
                               2, row * self.cell_width + self.cell_width//2), self.circle_radius)

    def draw_grid(self, screen) -> None:
        """Draws empty board on screen"""
        # self.screen.fill(Colors.BLACK)
        for row in range(self.rows):
            for col in range(self.cols):
                color = Colors.BROWN if (row+col) % 2 else Colors.WHITE
                pygame.draw.rect(screen, color, (row*self.cell_width, col*self.cell_width,
                                                 self.cell_width, self.cell_width))

    def get_piece(self, row, col):
        return self.grid[row, col]

    def get_winner(self):
        return self.winner

    def valid_square(self, row, col) -> bool:
        if row < 0 or row >= self.rows:
            return False
        if col < 0 or col >= self.cols:
            return False
        return True

    def apply_move(self, row: int, col: int, new_row: int, new_col: int, captured_pieces) -> None:
        """Moves piece from old position to new position"""
        piece = self.grid[row, col]
        self.grid[new_row, new_col] = piece
        self.grid[row, col] = 0

        self.remove_captured(captured_pieces)

        self.square = (new_row, new_col)
        self.previous_square = (row, col)

        if self.get_piece(new_row, new_col) == StoneEnum.WHITE.value and new_row == 0:
            self.grid[new_row, new_col] += 2  # promote white
        if self.get_piece(new_row, new_col) == StoneEnum.BLACK.value and new_row == self.rows - 1:
            self.grid[new_row, new_col] += 2

    def remove_captured(self, captured_pieces):
        for cap in captured_pieces:
            self.remove_piece(*cap)

    def remove_piece(self, row: int, col: int) -> None:
        """Remove piece from given position"""
        if self.grid[row, col] in (StoneEnum.WHITE.value, StoneEnum.WHITE_KING.value):
            self.white_count -= 1
            if self.white_count == 0:
                self.winner = StoneEnum.BLACK.value
        elif self.grid[row, col] in (StoneEnum.BLACK.value, StoneEnum.BLACK_KING.value):
            self.black_count -= 1
            if self.black_count == 0:
                self.winner = StoneEnum.WHITE.value
        self.grid[row, col] = 0

    def get_dirs(self, color):
        white_dirs = [(-1, 1), (-1, -1)]
        black_dirs = [(1, 1), (1, -1)]
        if color > 2:
            return white_dirs + black_dirs
        if color == StoneEnum.WHITE.value:
            return white_dirs
        elif color == StoneEnum.BLACK.value:
            return black_dirs
        assert False

    def is_opponent(self, piece, other):
        if other == 0:
            return False
        if piece == StoneEnum.WHITE.value or piece == StoneEnum.WHITE_KING.value:
            return other in (StoneEnum.BLACK.value, StoneEnum.BLACK_KING.value)
        if piece == StoneEnum.BLACK.value or piece == StoneEnum.BLACK_KING.value:
            return other in (StoneEnum.WHITE.value, StoneEnum.WHITE_KING.value)
        assert False

    def get_valid_moves_all_pieces(self, color):
        assert (color == StoneEnum.WHITE.value or color == StoneEnum.BLACK.value)

        all_valid_moves = {}
        max_captures = 0
        pieces = np.argwhere(self.grid == color)
        pieces = list(map(tuple, pieces))

        for piece in pieces:
            valid_moves = self.get_valid_moves(*piece, color)
            if len(valid_moves) > 0 and len(valid_moves[0][1]) > max_captures:
                all_valid_moves.clear()
                max_captures = len(valid_moves[0][1])
            if len(valid_moves) > 0 and len(valid_moves[0][1]) >= max_captures:
                all_valid_moves[piece] = valid_moves

        king_color = color + 2
        king_pieces = np.argwhere(self.grid == king_color)
        king_pieces = list(map(tuple, king_pieces))
        for king_piece in king_pieces:
            king_valid_moves = self.get_valid_moves(*king_piece, king_color)
            if len(king_valid_moves) > 0 and len(king_valid_moves[0][1]) > max_captures:
                all_valid_moves.clear()
                max_captures = len(king_valid_moves[0][1])

            if len(king_valid_moves) > 0 and len(king_valid_moves[0][1]) >= max_captures:
                all_valid_moves[king_piece] = king_valid_moves
        return all_valid_moves

    def get_valid_moves(self, row: int, col: int, piece_type: int, has_captured=False, captured_pieces=None):
        if captured_pieces is None:
            captured_pieces = []

        valid_moves = []

        dirs = self.get_dirs(piece_type)
        if not has_captured:  # just move
            for (dir_row, dir_col) in dirs:
                if not self.valid_square(row + dir_row, col + dir_col):
                    continue
                if self.grid[row + dir_row, col + dir_col] == 0:
                    valid_moves.append(
                        ((row + dir_row, col + dir_col), deepcopy(captured_pieces)))
        # try to capture
        for (dir_row, dir_col) in dirs:
            if not self.valid_square(row + 2*dir_row, col + 2*dir_col):
                continue
            if (self.is_opponent(piece_type, self.grid[row + dir_row, col + dir_col]) and  # capturing an opponent piece and landing on empty square
                    self.grid[row + 2*dir_row, col + 2*dir_col] == 0):
                if (row + dir_row, col + dir_col) in captured_pieces:  # has already captured the piece
                    continue
                captured_pieces.append((row + dir_row, col + dir_col))
                # want moves with more captures
                if len(valid_moves) > 0 and len(captured_pieces) > len(valid_moves[-1][1]):
                    valid_moves.clear()

                # append only moves with as many captures
                if len(valid_moves) == 0 or len(captured_pieces) >= len(valid_moves[-1][1]):
                    valid_moves.append(
                        ((row + 2*dir_row, col + 2*dir_col), deepcopy(captured_pieces)))

                longer_valid_moves = self.get_valid_moves(  # run it recursively
                    row + 2*dir_row, col + 2*dir_col, piece_type, True, deepcopy(captured_pieces))
                if len(longer_valid_moves) > 0:
                    if len(longer_valid_moves[-1][1]) > len(valid_moves[-1][1]):
                        valid_moves = longer_valid_moves
                    elif len(longer_valid_moves[-1][1]) == len(valid_moves[-1][1]):
                        valid_moves.extend(longer_valid_moves)
                captured_pieces.pop()

        return valid_moves
