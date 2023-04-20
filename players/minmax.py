import random
from itertools import product
from quinto import quinto
from .base import BasePlayer
from copy import deepcopy
import logging
import numpy as np

class MinmaxPlayer(BasePlayer):
    """Minmax player"""
    
    def __init__(self, quarto: quinto.Quarto, moving_first=False, max_depth=5) -> None:
        super().__init__(quarto)
        self._chosen_piece = None
        self._chosen_position = None
        self.moving_index = 0 if moving_first else 1
        self.max_depth = max_depth

    def choose_piece(self) -> int:
        if self._chosen_piece not in self._game.available_pieces:
            return random.choice(self.available_pieces)
        return self._chosen_piece
    
    def place_piece(self) -> tuple[int, int]:
        logging.debug("Minmax thinking...")
        self._minmax()
        return self._chosen_position
    
    def _minmax(self):
        if len(self._game.available_pieces) < self.max_depth:
            (position, piece), _ = self.__minmax_r(self.get_game())
            self._chosen_position = position
            self._chosen_piece = piece
        else:
            self._chosen_position = random.choice(self._game.available_position)
            self._chosen_piece = random.choice(self._game.available_pieces)

        
    def __minmax_r(self, state, alpha=-1, beta=1):
        maximising_player = self.moving_index == self._game.get_current_player()
        if state.check_winner() >= 0 or state.check_finished():
            # no more moves: state.player lost
            return None, 1 if not maximising_player else -1

        val = (None, -1) if maximising_player else (None, 1)
        for piece, position in product(state.available_pieces, state.available_position):
            new_state = deepcopy(state)
            new_state.place(*position)
            if len(new_state.available_pieces) > 0:
                new_state.select(piece)
            _, ns_value = self.__minmax_r(new_state, alpha, beta)

            if maximising_player:
                val = max(((position, piece), ns_value), val, key=lambda x: x[1])
                alpha = max(alpha, ns_value)
            else:
                val = min(((position, piece), ns_value), val, key=lambda x: x[1])
                beta = min(beta, ns_value)

            if (maximising_player and val[1] >= beta) or (not maximising_player and val[1] <= alpha):
                break
        return val