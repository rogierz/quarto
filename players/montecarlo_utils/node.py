import copy
import math
import random
import numpy as np
from quinto.quinto import Quarto


def calculate_uct(child_visits, wins, parent_visits):
    if parent_visits == 0 or child_visits == 0:
        return float('inf')
    return (wins / child_visits) + \
        (math.sqrt((2 * math.log(parent_visits)) / child_visits))


class Node:
    def __init__(self, parent=None, game: Quarto = None, piece=None):
        self.parent = parent
        self.stats = [0, 0]  # wins, visits
        self.actions = game.available_actions
        self.children = []
        self.score = float('inf')
        self.game = copy.deepcopy(game)
        self.piece = piece

        self.is_root = parent is None

    def __repr__(self):
        return "(" + str(self.game.get_board_status()) + ", " + \
            str(self.game.get_selected_piece()) + ")"

    def rollout(self):
        rollout_game = copy.deepcopy(self.game)
        spaces = copy.deepcopy(self.game.available_position)
        pieces = copy.deepcopy(self.game.available_pieces)
        next_piece = self.piece
        while len(spaces) > 0 and len(pieces) > 0:
            rollout_game.select(next_piece)
            rollout_game._current_player = (
                rollout_game._current_player + 1) % rollout_game.MAX_PLAYERS
            next_space = random.choice(spaces)
            rollout_game.place(next_space[0], next_space[1])
            winner = rollout_game.check_winner()
            end = winner >= 0 or rollout_game.check_finished()
            if end:
                if winner == self.game.get_current_player():
                    return True
                else:
                    return False
            next_piece = random.choice(pieces)
            spaces.remove(next_space)
            pieces.remove(next_piece)
        return False

    def backpropagate(self, simulated_result):
        if simulated_result:
            self.stats[0] += 1
        self.stats[1] += 1
        if self.is_root:
            return
        self.parent.backpropagate(simulated_result)

    def is_terminal_node(self):
        if self.game.check_finished() or self.game.check_winner() >= 0:
            return True
        return False

    def is_fully_expanded(self):
        if len(self.actions) == 0:
            return True
        return False

    def expand(self):
        next_action = random.choice(self.actions)
        next_piece = next_action[0]
        next_space = next_action[1]

        next_game = copy.deepcopy(self.game)
        next_game.place(next_space[0], next_space[1])

        child_node = Node(parent=self, game=next_game, piece=next_piece)
        self.children.append(child_node)
        return child_node

    def best_child(self):
        best_child = None
        if self.children:
            best_child = max(self.children, key=lambda child: child.stats[1])
        return best_child

    def best_uct(self):
        parent_visits = self.stats[1]
        best_utc_child = self.children[0]
        for child in self.children:
            child.score = calculate_uct(
                child.stats[1], child.stats[0], parent_visits)
            if child.score > best_utc_child.score:
                best_utc_child = child

        return best_utc_child
