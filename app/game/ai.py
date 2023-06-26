"""This module handles AI."""
import math
from copy import deepcopy
import random
import numpy as np
from game.config import StoneEnum
from game.board import Board
from game.config import AIConstants


class AI:
    """Class representing AI"""

    def __init__(self, color: int) -> None:
        self.color = color

    def get_best_move(self, board: Board):
        """Find best move"""
        evaluation, best_move = self.minimax(
            board, AIConstants.DEPTH, self.color == StoneEnum.WHITE.value, -math.inf, math.inf)
        print(f'EVAL = {evaluation}')
        return best_move

    def get_random_move(self, board: Board):
        """Gets random move for given position"""
        all_valid_moves = board.get_valid_moves_all_pieces(self.color)
        random.seed(AIConstants.SEED)
        piece = random.choice(list(all_valid_moves))
        dest, captured_pieces = random.choice(list(all_valid_moves[piece]))
        return piece, dest, captured_pieces

    @staticmethod
    def calc_winner(board: np.ndarray) -> None:
        """Checks if board has winner"""
        if (board == StoneEnum.WHITE.value).sum() +\
                (board == StoneEnum.WHITE_KING.value).sum() == 0:
            return -1
        if (board == StoneEnum.BLACK.value).sum() +\
                (board == StoneEnum.BLACK_KING.value).sum() == 0:
            return 1
        return 0

    def evaluate_board(self, board: np.ndarray):
        """First function to evaluate board"""
        score = 0
        # 10 points for every piece
        score += (board == StoneEnum.WHITE.value).sum() * 10
        score -= (board == StoneEnum.BLACK.value).sum() * 10

        # 15 points for every king
        score += (board == StoneEnum.WHITE_KING.value).sum() * 15
        score -= (board == StoneEnum.BLACK_KING.value).sum() * 15

        score += self.calc_winner(board) * 10000
        return score

    def evaluate_board2(self, board: np.ndarray):
        """Second function to evaluate board"""
        size = board.shape
        white_mask = np.zeros(size, dtype=int)
        for i in range(0, size[0] - 1, 2):
            white_mask[i:i+2, :] = size[0] - i
        black_mask = np.flip(-white_mask, axis=0)
        score = self.evaluate_board(board)
        score += white_mask[board == StoneEnum.WHITE.value].sum()
        score += black_mask[board == StoneEnum.BLACK.value].sum()
        return score

    @staticmethod
    def get_possible_positions(board: Board, color: int):
        """Gets all possible positions and moves to get there"""
        possible_boards = []
        all_valid_moves = board.get_valid_moves_all_pieces(color)
        for piece in all_valid_moves:
            for dest, captured_pieces in all_valid_moves[piece]:
                new_board = deepcopy(board)
                new_board.apply_move(*piece, *dest, captured_pieces)
                possible_boards.append(
                    (new_board, (piece, dest, captured_pieces)))

        return possible_boards

    def minimax(self, board: Board, depth: int, maximizing_player: bool, alpha, beta):
        """Implementation of MiniMax algorithm"""
        # pylint: disable=too-many-arguments
        if depth == 0 or self.calc_winner(board.grid) != 0:
            return self.evaluate_board2(board.grid), ()
        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for new_board, move in self.get_possible_positions(board, StoneEnum.WHITE.value):
                value = self.minimax(new_board, depth - 1,
                                     False, alpha, beta)[0]
                max_eval = max(max_eval, value)
                if value == max_eval:
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break

            return max_eval, best_move
        min_eval = math.inf
        best_move = None
        for new_board, move in self.get_possible_positions(board, StoneEnum.BLACK.value):
            value = self.minimax(new_board, depth - 1,
                                 True, alpha, beta)[0]
            min_eval = min(min_eval, value)
            if value == min_eval:
                best_move = move
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, best_move
