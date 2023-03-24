import numpy as np
from quarto import quarto
from copy import deepcopy
from functools import reduce

class BasePlayer(quarto.Player):
    """Base class for creating an agent"""

    def __init__(self, quarto: quarto.Quarto):
        super().__init__(quarto)

    def __str__(self):
        return type(self).__name__
    
    def _get_board(self):
        game = self.get_game()
        board = game.get_board_status()
        return board
    
    def _simulate_winning_move(self, position, piece=None):
        quarto = deepcopy(self.get_game())
        if piece:
            quarto.select(piece)
        quarto.place(position[0], position[1])
        return quarto.check_winner() != -1
    
    def _update_pieces(self):
        board = self._get_board()
        pieces_index = np.where(board != -1)
        placed_pieces_on_board = board[pieces_index]
        for i in placed_pieces_on_board:
            if i in self.available_pieces:
                self.available_pieces.remove(i)

    def _update_positions(self):
        board = self._get_board()
        pieces_index = np.where(board != -1)
        for i in range(len(pieces_index[0])):
            tuple_index = (pieces_index[1][i], pieces_index[0][i])
            if tuple_index in self.available_position:
                self.available_position.remove(tuple_index)

    def _check_winning_position(self, positions, partial_board):
        if positions.shape[0] == 1:
            binary_representation = partial_board
            binary_representation = binary_representation[binary_representation != -1]
            common_pieces_1 = reduce(lambda a, b: a & b, binary_representation)
            common_pieces_2 = reduce(lambda a, b: a & (not b), binary_representation, 15)
            return common_pieces_1 or common_pieces_2
        return False

    def _list_winning_positions(self):
        # 1 check if it's the last position where to place a piece
        winning_position = []

        if len(self.available_pieces) > 12:
            return winning_position

        board = self._get_board()

        for i in range(4):
            column_pos = np.where(board[i, :] == -1)[0]
            if self._check_winning_position(column_pos, board[i, :]):
                winning_position.append((column_pos[0], i))

            row_pos = np.where(board[:, i] == -1)[0]
            if self._check_winning_position(row_pos, board[:, i]):
                winning_position.append((i, row_pos[0]))

        diag_1 = np.diag(board)
        diag1_pos = np.where(diag_1 == -1)[0]
        if self._check_winning_position(diag1_pos, diag_1):
            winning_position.append((diag1_pos[0], diag1_pos[0]))

        diag_2 = np.diag(np.fliplr(board))
        diag2_pos = np.where(diag_2 == -1)[0]
        if self._check_winning_position(diag2_pos, diag_2):
            winning_position.append((3 - diag2_pos[0], diag2_pos[0]))

        return winning_position