"""https://scholarworks.umt.edu/cgi/viewcontent.cgi?article=1334&context=tme"""

from quinto import quinto
import random
import numpy as np
from copy import deepcopy
from functools import reduce
from .base import BasePlayer


class RiskyPlayer(BasePlayer):

    def __init__(self, quarto: quinto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        # check if there is a winning position for the opponent
        winning_position_opponent = self._list_winning_positions()
        if len(winning_position_opponent) > 0:
            # if there is a winning position for the opponent then delete the
            # pieces that makes them winning
            available_pieces = deepcopy(self._game.available_pieces)
            for position in winning_position_opponent:
                for piece in available_pieces:
                    winner = self._simulate_winning_move(position, piece)
                    if winner:
                        available_pieces.remove(piece)
            if len(available_pieces) > 0:
                return random.choice(available_pieces)

        piece = random.choice(self._game.available_pieces)
        return piece

    def __check_line_position(self, positions, partial_board):
        if positions.shape[0] <= 3 and positions.shape[0]:
            quarto = self.get_game()
            piece = quarto.get_selected_piece()
            binary_representation = deepcopy(partial_board)
            binary_representation[positions[0]] = piece
            binary_representation = binary_representation[binary_representation != -1]
            common_pieces_1 = reduce(lambda a, b: a & b, binary_representation)
            common_pieces_2 = reduce(
                lambda a, b: a & (
                    not b), binary_representation, 15)
            return common_pieces_1 or common_pieces_2
        return False

    def __check_line_positions(self):

        board = self._get_board()
        line_position_3_vacancy = []
        line_position_2_vacancy = []

        for i in range(4):
            column_pos = np.where(board[i, :] == -1)[0]
            if self.__check_line_position(column_pos, board[i, :]):
                if len(column_pos) == 3:
                    line_position_3_vacancy.append((column_pos[0], i))
                else:
                    line_position_2_vacancy.append((column_pos[0], i))

            row_pos = np.where(board[:, i] == -1)[0]
            if self.__check_line_position(row_pos, board[:, i]):
                if len(row_pos) == 3:
                    line_position_3_vacancy.append((i, row_pos[0]))
                else:
                    line_position_2_vacancy.append((i, row_pos[0]))

        diag_1 = np.diag(board)
        diag1_pos = np.where(diag_1 == -1)[0]
        if self.__check_line_position(diag1_pos, diag_1):
            if len(diag1_pos) == 3:
                line_position_3_vacancy.append((diag1_pos[0], diag1_pos[0]))
            else:
                line_position_2_vacancy.append((diag1_pos[0], diag1_pos[0]))

        diag_2 = np.diag(np.fliplr(board))
        diag2_pos = np.where(diag_2 == -1)[0]
        if self.__check_line_position(diag2_pos, diag_2):
            if len(diag2_pos) == 3:
                line_position_3_vacancy.append(
                    (3 - diag2_pos[0], diag2_pos[0]))
            else:
                line_position_2_vacancy.append(
                    (3 - diag2_pos[0], diag2_pos[0]))

        if len(line_position_2_vacancy) > 0:
            return line_position_2_vacancy
        return line_position_3_vacancy

    def place_piece(self) -> tuple[int, int]:
        candidate_winning_position = self._list_winning_positions()
        if len(candidate_winning_position) > 0:
            for position in candidate_winning_position:
                winner = self._simulate_winning_move(position)
                if winner:
                    return position[0], position[1]

        candidate_line_position = self.__check_line_positions()

        if len(candidate_line_position) > 0:
            return candidate_line_position[0][0], candidate_line_position[0][1]

        x, y = random.choice(self._game.available_position)
        return x, y
