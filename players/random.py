import random
from quarto import quarto
from .base import BasePlayer
import numpy as np


class RandomPlayer(BasePlayer):
    """Random player"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.available_position = [(i, j) for i in range(4) for j in range(4)]
        self.available_pieces = [i for i in range(16)]

    def choose_piece(self) -> int:
        self._update_pieces()
        piece = random.choice(self.available_pieces)
        return piece

    def place_piece(self) -> tuple[int, int]:
        self._update_positions()
        x, y = random.choice(self.available_position)
        return x, y
