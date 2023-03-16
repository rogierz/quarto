import random
from quarto import quarto
import numpy as np


class RandomPlayer(quarto.Player):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.available_position = [(i, j) for i in range(4) for j in range(4)]
        self.available_pieces = [i for i in range(16)]

    def __get_board(self):
        game = self.get_game()
        board = game.get_board_status()
        return board

    def __update_pieces(self):
        board = self.__get_board()
        pieces_index = np.where(board != -1)
        placed_pieces_on_board = board[pieces_index]
        for i in placed_pieces_on_board:
            if i in self.available_pieces:
                self.available_pieces.remove(i)

    def __update_positions(self):
        board = self.__get_board()
        pieces_index = np.where(board != -1)
        for i in range(len(pieces_index[0])):
            tuple_index = (pieces_index[1][i], pieces_index[0][i])
            if tuple_index in self.available_position:
                self.available_position.remove(tuple_index)

    def choose_piece(self) -> int:
        self.__update_pieces()
        piece = random.choice(self.available_pieces)
        return piece

    def place_piece(self) -> tuple[int, int]:
        self.__update_positions()
        x, y = random.choice(self.available_position)
        return x, y
