"""https://scholarworks.umt.edu/cgi/viewcontent.cgi?article=1334&context=tme"""

import random
from copy import deepcopy
from quinto import quinto
from .base import BasePlayer


class NaivePlayer(BasePlayer):

    def __init__(self, quarto: quinto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        # check if there is a winning position for the opponent
        winning_position_opponent = self._list_winning_positions()
        if len(winning_position_opponent) > 0:
            # if there is a winning position for the opponent then delete the pieces that makes them winning
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

    def place_piece(self) -> tuple[int, int]:
        candidate_winning_position = self._list_winning_positions()
        if len(candidate_winning_position) > 0:
            for position in candidate_winning_position:
                winner = self._simulate_winning_move(position)
                if winner:
                    return position[0], position[1]

        x, y = random.choice(self._game.available_position)
        return x, y
