import random
from itertools import product
from quarto import quarto
from .base import BasePlayer
from copy import deepcopy
import logging
import numpy as np

class MinmaxPlayer(BasePlayer):
    """Minmax player"""
    
    def __init__(self, quarto: quarto.Quarto, moving_first=False, max_depth=3) -> None:
        super().__init__(quarto)
        self.available_position = [(i, j) for i in range(4) for j in range(4)]
        self.available_pieces = [i for i in range(16)]
        self._chosen_piece = None
        self._chosen_position = None
        self.moving_index = 0 if moving_first else 1
        self.max_depth = max_depth


    def _update(self):
        self._update_pieces()
        self._update_positions()

    def choose_piece(self) -> int:
        self._update()
        if self._chosen_piece not in self.available_pieces:
            return random.choice(self.available_pieces)
        return self._chosen_piece
    
    def place_piece(self) -> tuple[int, int]:
        self._update()
        logging.debug("Minmax thinking...")
        self._minmax()
        return self._chosen_position
    
    def _minmax(self):
        if len(self.available_pieces) <= self.max_depth:
            (position, piece), _ = self.__minmax_r(self.get_game())
            self._chosen_position = position
            self._chosen_piece = piece
        
        if len(self.available_pieces) > self.max_depth or self._chosen_position is None or self._chosen_piece is None:
            self._chosen_position = random.choice(self.available_position)
            self._chosen_piece = random.choice(self.available_pieces)

        assert self._chosen_piece is not None
        assert self._chosen_position is not None
        
    def __minmax_r(self, state, alpha=-1, beta=1, depth=0):
        logging.warning(f"Recurring in depth {depth}")
        maximising_player = self.moving_index == self.get_game().get_current_player()
        # placing_piece = self.get_game().get_selected_piece()
        if state.check_winner() >= 0 or state.check_finished():
            # no more moves: state.player lost
            return (None, None), 1 if not maximising_player else -1

        val = ((None, None), -1) if maximising_player else ((None, None), 1)
        for piece, position in product(self.available_pieces, self.available_position):
            new_state = self.get_game()
            new_state.place(*position)
            new_state.select(piece)
            _, ns_value = self.__minmax_r(new_state, alpha, beta, depth=depth+1)

            if maximising_player:
                val = max(((position, piece), ns_value), val, key=lambda x: x[1])
                alpha = max(alpha, ns_value)
            else:
                val = min(((position, piece), ns_value), val, key=lambda x: x[1])
                beta = min(beta, ns_value)

            if (maximising_player and val[1] >= beta) or (not maximising_player and val[1] <= alpha):
                break
        return val