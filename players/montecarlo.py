from quarto import quarto
from copy import deepcopy
from players.montecarlo_utils.montecarlo_tree_search import monte_carlo_tree_search
from players.montecarlo_utils.node import Node
import random


class MonteCarloPlayer(quarto.Player):
    """Base class for creating an agent"""

    def __init__(self, quarto: quarto.Quarto):
        super().__init__(quarto)
        self.next_piece = None
        self.space = None

    def __str__(self):
        return type(self).__name__

    def choose_piece(self) -> int:
        return self.next_piece if self.next_piece else random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        game = self.get_game()
        piece = game.get_selected_piece()
        node = Node(game=game, piece=piece)
        piece, space, ret, n, elapsed, nodesexpanded = monte_carlo_tree_search(root=node, maxtime=1, maxnodes=10)
        self.next_piece = deepcopy(piece)

        return space[1], space[0]