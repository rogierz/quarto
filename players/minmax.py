import random
from itertools import product
from quinto import quinto
from .base import BasePlayer
from copy import deepcopy
import logging


class MinmaxPlayer(BasePlayer):
    """Minmax player"""

    def __init__(self, quarto: quinto.Quarto, max_depth=5) -> None:
        super().__init__(quarto)
        self._chosen_piece = None
        self._chosen_position = None
        self.max_depth = max_depth

    def choose_piece(self) -> int:
        if self._chosen_piece not in self._game.available_pieces:
            return random.choice(self._game.available_pieces)
        return self._chosen_piece

    def place_piece(self) -> tuple[int, int]:
        logging.debug("Minmax thinking...")
        self._minmax()
        return self._chosen_position

    def _minmax(self):
        if len(self._game.available_pieces) < self.max_depth:
            (position, piece), _ = self.__minmax_r(self.get_game(), player=self.moving_index)
            self._chosen_position = position
            self._chosen_piece = piece
        else:
            self._chosen_position = random.choice(self._game.available_position)
            self._chosen_piece = random.choice(self._game.available_pieces)

    def __minmax_r(self, state, player, alpha=float('-inf'), beta=float('+inf')):
        maximising_player = self.moving_index == self._game.get_current_player()
        if state.check_winner() >= 0 or state.check_finished():
            # no more moves: state.player lost
            value = 1 if not maximising_player else -1
            return (self._game.available_position[0], None), value

        val = ((self._game.available_position[0], None), -1) if maximising_player else ((self._game.available_position[0], None), 1)
        for piece, position in product(state.available_pieces, state.available_position):
            new_state = deepcopy(state)
            new_state.place(*position)
            if len(new_state.available_pieces) > 0:
                new_state.select(piece)
            _, ns_value = self.__minmax_r(new_state, 1 - player, alpha, beta)

            if player == self.moving_index:
                val = max(((position, piece), ns_value), val, key=lambda x: x[1])
                alpha = max(alpha, ns_value)
            else:
                val = min(((position, piece), ns_value), val, key=lambda x: x[1])
                beta = min(beta, ns_value)

            if beta <= alpha:
                break
        return val
