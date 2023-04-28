from quarto import quarto
from copy import deepcopy
from players.montecarlo_utils.montecarlo import MonteCarlo
from .base import BasePlayer
import random


class MonteCarloPlayer(BasePlayer):

    def __init__(self, quarto: quarto.Quarto):
        super().__init__(quarto)
        self.next_piece = None

    def __str__(self):
        return type(self).__name__

    def choose_piece(self) -> int:
        return self.next_piece if self.next_piece else random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        game = self.get_game()
        montecarlo = MonteCarlo(game=game)
        next_piece, space = montecarlo.search()
        self.next_piece = deepcopy(next_piece)

        return space[0], space[1]
