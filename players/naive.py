"""https://scholarworks.umt.edu/cgi/viewcontent.cgi?article=1334&context=tme"""
import gc
from copy import deepcopy

from quarto import quarto
import random
import numpy as np
from functools import reduce


class NaivePlayer(quarto.Player):

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.available_position = [(i, j) for i in range(4) for j in range(4)]
        self.available_pieces = [i for i in range(16)]

    def __get_board(self):
        game = self.get_game()
        board = game.get_board_status()
        return board

    def __simulate_winning_move(self, position, piece=None):
        quarto = deepcopy(self.get_game())
        if piece:
            quarto.select(piece)
        quarto.place(position[0], position[1])
        return quarto.check_winner() != -1

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

    def __check_winning_position(self, positions, partial_board):
        if positions.shape[0] == 1:
            binary_representation = partial_board
            binary_representation = binary_representation[binary_representation != -1]
            common_pieces_1 = reduce(lambda a, b: a & b, binary_representation)
            common_pieces_2 = reduce(lambda a, b: a & (not b), binary_representation, 15)
            return common_pieces_1 or common_pieces_2
        return False

    def __list_winning_positions(self):
        # 1 check if it's the last position where to place a piece
        winning_position = []

        if len(self.available_pieces) > 12:
            return winning_position

        board = self.__get_board()

        for i in range(4):
            column_pos = np.where(board[i, :] == -1)[0]
            if self.__check_winning_position(column_pos, board[i, :]):
                winning_position.append((column_pos[0], i))

            row_pos = np.where(board[:, i] == -1)[0]
            if self.__check_winning_position(row_pos, board[:, i]):
                winning_position.append((i, row_pos[0]))

        diag_1 = np.diag(board)
        diag1_pos = np.where(diag_1 == -1)[0]
        if self.__check_winning_position(diag1_pos, diag_1):
            winning_position.append((diag1_pos[0], diag1_pos[0]))

        diag_2 = np.diag(np.fliplr(board))
        diag2_pos = np.where(diag_2 == -1)[0]
        if self.__check_winning_position(diag2_pos, diag_2):
            winning_position.append((3 - diag2_pos[0], diag2_pos[0]))

        return winning_position

    def choose_piece(self) -> int:
        self.__update_pieces()
        # check if there is a winning position for the opponent
        winning_position_opponent = self.__list_winning_positions()
        if len(winning_position_opponent) > 0:
            # if there is a winning position for the opponent then delete the pieces that makes them winning
            available_pieces = deepcopy(self.available_pieces)
            for position in winning_position_opponent:
                for piece in available_pieces:
                    winner = self.__simulate_winning_move(position, piece)
                    if winner:
                        available_pieces.remove(piece)
            if len(available_pieces) > 0:
                return random.choice(available_pieces)

        piece = random.choice(self.available_pieces)
        return piece

    def place_piece(self) -> tuple[int, int]:
        self.__update_positions()
        candidate_winning_position = self.__list_winning_positions()
        if len(candidate_winning_position) > 0:
            for position in candidate_winning_position:
                winner = self.__simulate_winning_move(position)
                if winner:
                    return position[0], position[1]

        x, y = random.choice(self.available_position)
        return x, y
