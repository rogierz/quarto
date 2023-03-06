"""https://scholarworks.umt.edu/cgi/viewcontent.cgi?article=1334&context=tme"""
from copy import deepcopy

from quarto import quarto
import random
import numpy as np

class NaivePlayer(quarto.Player):

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.available_position = [(i, j) for i in range(4) for j in range(4)]
        self.available_pieces = [i for i in range(16)]

    def __update(self):
        game = self.get_game()
        board = game.get_board_status()
        pieces_index = np.where(board != -1)
        placed_pieces_on_board = board[pieces_index]
        for i in placed_pieces_on_board:
            if i in self.available_pieces:
                self.available_pieces.remove(i)

        for i in range(len(pieces_index[0])):
            tuple_index = (pieces_index[1][i], pieces_index[0][i])
            if tuple_index in self.available_position:
                self.available_position.remove(tuple_index)

    def check_winning_position(self):
        # 1 check if it's the last position where to place a piece
        game = self.get_game()
        board = game.get_board_status()
        for i in range(4):
            column_pos = np.where(board[i][:] == -1)
            row_pos = np.where(board[:][i] == -1)
            if row_pos.shape[0] == 1 and column_pos.shape[0] == 1:
                return column_pos

        diag_1 = np.trace(board, axis1=0, axis2=1)
        diag_2 = np.trace(np.fliplr(board), axis1=0, axis2=1)

        diag1_pos = np.where(diag_1 == -1)
        if diag1_pos.shape[0] == 1:
            return (diag1_pos, diag1_pos)

        diag2_pos = np.where(diag_2 == -1)
        if diag2_pos.shape[0] == 1:
            return (3 - diag2_pos, diag2_pos)

        return (None, None)

    # 2 check if it's a winning position for the opponent

    def choose_piece(self) -> int:
        self.__update()
        # check if there is a winning position for the opponent
        winning_position_opponent = self.check_winning_position()
        if winning_position_opponent:
            # if there is a winning position for the opponent then delete the pieces that makes them winning
            quarto = deepcopy(self.get_game())
            for piece in self.available_pieces:
                quarto.select(piece)
                quarto.place(winning_position_opponent[0], winning_position_opponent[1])
                if quarto.check_winner():
                    self.available_pieces.remove(piece)
            return random.choice(self.available_pieces)
        else:
            return random.choice(self.available_pieces)

    def place_piece(self) -> tuple[int, int]:
        self.__update()
        winning_position = self.check_winning_position()
        if winning_position:
            for piece in self.available_pieces:
                quarto = deepcopy(self.get_game())
                quarto.place(winning_position[0], winning_position[1])
                if quarto.check_winner():
                    return winning_position[0], winning_position[1]
        else:
            return np.random.choice(self.available_position)





