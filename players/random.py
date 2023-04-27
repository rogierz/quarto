import random
from quinto import quinto
from .base import BasePlayer


class RandomPlayer(BasePlayer):
    """Random player"""

    def __init__(self, quarto: quinto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        piece = random.choice(self._game.available_pieces)
        return piece

    def place_piece(self) -> tuple[int, int]:
        x, y = random.choice(self._game.available_position)
        return x, y
