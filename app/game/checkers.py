"Module representing checkers game interface"
from copy import deepcopy
import pygame
from game.board import Board
from game.config import SizeConstants as const
from game.config import StoneEnum
from game.config import WINNER_FONT
from game.config import Colors


class Checkers:
    """Class representing game of checkers"""

    def __init__(self, screen) -> None:
        self.screen = screen
        self.board = Board(const.ROWS, const.COLS,
                           const.CELL_SIZE, const.CIRCLE_RADIUS)
        self.turn = StoneEnum.WHITE.value

        self.all_pieces_valid_moves = self.board.get_valid_moves_all_pieces(
            self.turn)
        # print(str(self.turn) + ': ')
        # print(self.all_pieces_valid_moves)
        # print()
        self.selected_piece = None
        self.valid_moves = None

        self.move_count = 0

    def update_screen(self) -> None:
        """Update game on screen"""
        self.board.draw_all(self.screen)
        if self.selected_piece is not None:
            self.board.highlight(self.screen, *self.selected_piece)
            self.board.draw_valid_moves(self.screen, self.valid_moves)
        self.board.draw_pieces(self.screen)
        pygame.display.update()

    def draw_winner(self, text):
        """Draw Winner name on screen"""
        draw_text = WINNER_FONT.render('WINNER: ' + text, 1, Colors.BLACK)
        self.screen.blit(draw_text, (const.WIDTH/2 - draw_text.get_width() /
                            2, const.HEIGHT/2 - draw_text.get_height()/2))
        # print(f'WINNER: {text} ')  # MAC
        # print(f'MOVE COUNT: {self.move_count}')
        pygame.display.update()
        pygame.time.delay(5000)

    def check_winner(self, draw=True) -> None:
        """Check if winner is to be crowned"""
        winner = self.board.get_winner()
        if not draw and (winner or len(self.all_pieces_valid_moves) == 0):
            return True
        if len(self.all_pieces_valid_moves) == 0:
            if self.on_turn(StoneEnum.BLACK.value):
                self.draw_winner('WHITE')
            else:
                self.draw_winner('BLACK')
            return True
        if winner is None:
            return False
        if winner == StoneEnum.WHITE.value:
            self.draw_winner('WHITE')
        else:
            self.draw_winner('BLACK')
        return True

    @staticmethod
    def get_clicked_pos(pos) -> tuple[int, int]:
        """Convert pygame pos to game board position"""
        x_pos, y_pos = pos
        row = y_pos // const.CELL_SIZE
        col = x_pos // const.CELL_SIZE
        return row, col

    def get_board(self):
        """Retrieve game board"""
        return deepcopy(self.board)

    def find_move(self, row, col):
        """Find move with given target from all valid moves"""
        for dest, captured_pieces in self.valid_moves:
            if dest == (row, col):
                return captured_pieces
        return False

    def try_move(self, row, col) -> bool:
        """Try given move"""
        captured_pieces = self.find_move(row, col)
        if captured_pieces is False:  # not in valid moves
            return False

        # move piece
        self.board.apply_move(*self.selected_piece, row, col, captured_pieces)

        self.selected_piece = None
        self.valid_moves = None
        if self.on_turn(StoneEnum.WHITE.value):
            self.move_count += 1
        self.change_turn()
        self.all_pieces_valid_moves = self.board.get_valid_moves_all_pieces(
            self.turn)
        print(str(self.turn) + ': ')
        print(self.all_pieces_valid_moves)
        print()
        return True

    def process_input(self, pos) -> None:
        """Process input from mouse"""
        row, col = self.get_clicked_pos(pos)
        if not self.board.valid_square(row, col):
            return
        if (row, col) == self.selected_piece:
            # print(self.valid_moves)
            return
        # print(f'Clicked on {row}, {col}')
        # print(self.valid_moves)
        if self.selected_piece is None:
            if not self.on_turn(self.board.get_piece(row, col)):
                return
            self.selected_piece = (row, col)
            # color = int(self.board.get_piece(*self.selected_piece).copy())
            self.valid_moves = self.all_pieces_valid_moves.get(
                self.selected_piece, ())
            return
        if self.on_turn(self.board.get_piece(row, col)):
            self.selected_piece = (row, col)
            self.valid_moves = self.all_pieces_valid_moves.get(
                self.selected_piece, ())
            return
        self.try_move(row, col)

    def on_turn(self, color) -> bool:
        """Check who is on turn"""
        if self.turn == StoneEnum.WHITE.value:
            return color in (self.turn, StoneEnum.WHITE_KING.value)
        return color in (self.turn, StoneEnum.BLACK_KING.value)

    def change_turn(self) -> None:
        """Change turn from WHITE to BLACK or reverse"""
        if self.turn == StoneEnum.WHITE.value:
            self.turn = StoneEnum.BLACK.value
        else:
            self.turn = StoneEnum.WHITE.value

    def ai_move(self, move):
        """Apply move from AI"""
        piece, dest, captured_pieces = move
        assert self.on_turn(self.board.get_piece(*piece))
        if self.on_turn(StoneEnum.WHITE.value):
            self.move_count += 1
        self.board.apply_move(*piece, *dest, captured_pieces)

        self.selected_piece = None
        self.valid_moves = None
        self.change_turn()
        self.all_pieces_valid_moves = self.board.get_valid_moves_all_pieces(
            self.turn)
        print(str(self.turn) + ': ')
        print(self.all_pieces_valid_moves)
        print()
        pygame.time.delay(100)
        return True
