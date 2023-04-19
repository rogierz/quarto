import random
import time
import numpy as np
import logging
from quarto.quarto import Quarto
from .node import Node


class MonteCarlo:

    def __init__(self, game: Quarto, budget_time: float = 10000, max_nodes: int = 2000):

        self.game = game
        self.root_node = Node(game=game)
        self.time_budget = budget_time
        self.max_expanded_nodes = max_nodes
        self.current_expanded_nodes = 0
        self.elapsed_time = 0.0

    def search(self):

        start_time = time.time()
        while self.available_resources():
            leaf = self.traverse()
            simulation_result = leaf.rollout()
            leaf.backpropagate(simulation_result)

            # stats
            self.current_expanded_nodes += 1
            self.elapsed_time = time.time() - start_time

        best_child = self.root_node.best_child()
        index_selected_piece = best_child.game.get_selected_piece()
        board_status = best_child.game.get_board_status()
        space = np.where(board_status == index_selected_piece)
        space = (space[1][0], space[0][0])

        if best_child.is_terminal_node():
            next_piece = None
        elif best_child.best_child() is None:
            action = random.choice(best_child.actions)
            next_piece = action[0]
        else:
            next_piece = best_child.best_child().piece

        return next_piece, space

    def available_resources(self):
        if self.elapsed_time > self.time_budget:
            # logging.warning(f"montecarlo: truncated -> exceeded time resources")
            return False

        if self.current_expanded_nodes > self.max_expanded_nodes:
            # logging.warning(f"montecarlo: truncated -> exceeded memory resources")
            return False

        return True

    def traverse(self):
        current_node = self.root_node
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = self.root_node.best_uct()

        return current_node
