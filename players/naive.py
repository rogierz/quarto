"""https://scholarworks.umt.edu/cgi/viewcontent.cgi?article=1334&context=tme"""

from quarto import quarto
import random

class NaivePlayer(quarto.Player):


    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)


    def choose_piece(self) -> int:
        #print(dir(self))
        #print(self._Player__quarto.get_board_status())
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)


