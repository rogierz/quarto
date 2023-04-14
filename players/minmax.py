import random
from itertools import product
from quarto import quarto
from .base import BasePlayer
from copy import deepcopy
import numpy as np

class MinmaxPlayer(BasePlayer):
    """Minmax player"""
    
    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.available_position = [(i, j) for i in range(4) for j in range(4)]
        self.available_pieces = [i for i in range(16)]
        self._chosen_piece = None
        self._chosen_position = None

    def _update(self):
        self._update_pieces()
        self._update_positions()

    def choose_piece(self) -> int:
        self._update()
        self._minmax()
        return self._chosen_piece
    
    def place_piece(self) -> tuple[int, int]:
        return self._chosen_position
    
    def _minmax(self, state, alpha=-1, beta=1):
        maximising_player = state.player == 0

        if state.check_winner() >= 0 or state.check_finished():
            # no more moves: state.player lost
            return None, 1 if not maximising_player else -1

        val = (None, -1) if maximising_player else (None, 1)
        for piece, position in product(self.available_pieces, self.available_position):
            new_state = deepcopy(self.get_game())
            new_state.select(piece)
            new_state.place(*position)
            _, ns_value = self._minmax(new_state, alpha, beta)

            if maximising_player:
                val = max((piece, position, ns_value), val, key=lambda x: x[1])
                alpha = max(alpha, ns_value)
            else:
                val = min((piece, position, ns_value), val, key=lambda x: x[1])
                beta = min(beta, ns_value)

            
            if (maximising_player and val[1] >= beta) or (not maximising_player and val[1] <= alpha):
                break
        return val