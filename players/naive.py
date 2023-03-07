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

        print('here_2')

    def __check_position(self, positions, partial_board):

        if positions.shape[0] == 1:
            binary_representation = partial_board
            binary_representation = binary_representation[binary_representation != -1]
            common_pieces_1 = reduce(lambda a, b: a & b, binary_representation)
            common_pieces_2 = reduce(lambda a, b: a & (not b), binary_representation, 15)
            return common_pieces_1 or common_pieces_2
        return False


    def __check_winning_positions(self):
        # 1 check if it's the last position where to place a piece

        if len(self.available_pieces) > 12:
            return []

        winning_position = []
        game = self.get_game()
        board = game.get_board_status()
        for i in range(4):
            column_pos = np.where(board[i, :] == -1)[0]
            if self.__check_position(column_pos, board[i, :]):
                winning_position.append((column_pos[0], i))
            # if column_pos.shape[0] == 1:
            #     # check if is a winning position for the opponent
            #     binary_column = board[i][:]
            #     binary_column = binary_column[binary_column != -1]
            #     binary_column_1 = reduce(lambda a, b: a & b, binary_column)
            #     binary_column_2 = reduce(lambda a, b: a & (not b), binary_column, 15)
            #     if binary_column_1 or binary_column_2:
            #         winning_position.append((i, column_pos[0]))
            row_pos = np.where(board[:, i] == -1)[0]
            if self.__check_position(row_pos, board[:, i]):
                winning_position.append((i, row_pos[0]))
            # if row_pos.shape[0] == 1:
            #     winning_position.append((row_pos[0], i))

        diag_1 = np.diag(board)
        diag1_pos = np.where(diag_1 == -1)[0]
        if self.__check_position(diag1_pos, diag_1):
            winning_position.append((diag1_pos[0], diag1_pos[0]))
        diag_2 = np.diag(np.fliplr(board))
        diag2_pos = np.where(diag_2 == -1)[0]
        if self.__check_position(diag2_pos, diag_2):
            winning_position.append((3 - diag2_pos[0], diag2_pos[0]))




        # if diag1_pos.shape[0] == 1:
        #     winning_position.append((diag1_pos[0], diag1_pos[0]))


        # if diag2_pos.shape[0] == 1:
        #     winning_position.append((3 - diag2_pos[0], diag2_pos[0]))
        print('here_3')
        return winning_position

    # 2 check if it's a winning position for the opponent

    def choose_piece(self) -> int:
        self.__update()
        # check if there is a winning position for the opponent
        winning_position_opponent = self.__check_winning_positions()
        if len(winning_position_opponent) > 0:
            # if there is a winning position for the opponent then delete the pieces that makes them winning
            available_pieces = deepcopy(self.available_pieces)
            for position in winning_position_opponent:
                quarto = deepcopy(self.get_game())
                for piece in available_pieces:
                    quarto.select(piece)
                    quarto.place(position[0], position[1])
                    if quarto.check_winner() != -1:
                        available_pieces.remove(piece)
            if len(available_pieces) > 0:
                return random.choice(available_pieces)
            else:
                print('here')
                return random.choice(self.available_pieces)
        else:
            piece = random.choice(self.available_pieces)
            return piece

    def __possible_placement(self, candidate_position):
        for position in candidate_position:
            quarto = deepcopy(self.get_game())
            quarto.place(position[0], position[1])
            if quarto.check_winner() != -1:
                return position[0], position[1]
        return None, None



    def place_piece(self) -> tuple[int, int]:
        self.__update()
        candidate_winning_position = self.__check_winning_positions()
        if len(candidate_winning_position) > 0:
            position = self.__possible_placement(candidate_winning_position)
            if all(position):
                return position[0], position[1]
            else:
                x, y = random.choice(self.available_position)
                return x, y
        else:
            x, y = random.choice(self.available_position)
            return x, y
