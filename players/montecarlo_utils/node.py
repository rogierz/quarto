import copy
import math
import random
import numpy as np
from quarto.quarto import Quarto


def calculate_uct(child_visits, wins, parent_visits):
    if parent_visits == 0 or child_visits == 0:
        return float('inf')
    return (wins / child_visits) + (math.sqrt((2 * math.log(parent_visits)) / child_visits))


class Node:
    def __init__(self, parent=None, game: Quarto = None, piece=None):
        self.parent = parent  # piece given by parent (add to board when spawning children)
        self.stats = [0, 0]  # wins, visits
        self.actions = []
        self.children = []
        self.score = float('inf')
        self.game = game
        self.available_position = [(i, j) for i in range(4) for j in range(4)]
        self.available_pieces = [i for i in range(16)]
        self.piece = piece

        self.is_root = parent is None

        self._update_pieces()
        self._update_positions()

        if self.game is not None:
            pieces = self.available_pieces
            for p in pieces:
                for space in self.available_position:
                    self.actions.append([p, space])

    def __repr__(self):
        return "(" + str(self.game.get_board_status()) + ", " + str(self.game.get_selected_piece()) + ")"

    def _update_pieces(self):
        board = self.game.get_board_status()
        pieces_index = np.where(board != -1)
        placed_pieces_on_board = board[pieces_index]
        for i in placed_pieces_on_board:
            if i in self.available_pieces:
                self.available_pieces.remove(i)

    def _update_positions(self):
        board = self.game.get_board_status()
        pieces_index = np.where(board != -1)
        for i in range(len(pieces_index[0])):
            tuple_index = (pieces_index[1][i], pieces_index[0][i])
            if tuple_index in self.available_position:
                self.available_position.remove(tuple_index)

    def rollout(self):
        player = 0
        rollout_game = copy.deepcopy(self.game)
        spaces = copy.deepcopy(self.available_position)
        pieces = copy.deepcopy(self.available_pieces)
        while len(spaces) > 0 and len(pieces) > 0:
            next_space = random.choice(spaces)
            rollout_game.place(next_space[0], next_space[1])
            next_piece = random.choice(pieces)
            rollout_game.select(next_piece)

            winner = rollout_game.check_winner()

            end = winner >= 0 or rollout_game.check_finished()
            if end:
                if player % 2 == 0 and winner != -1:
                    return True
                else:
                    return False
            player = player + 1
            spaces.remove(next_space)
            pieces.remove(next_piece)
        return False

    def backpropagate(self, result):
        if result:
            self.stats[0] += 1
        self.stats[1] += 1
        if self.is_root:
            return
        self.parent.backpropagate(result)

    def is_terminal_node(self):
        if len(self.children) == 0 and len(self.actions) == 0:
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

            nextgame = copy.deepcopy(self.game)
            nextgame.place(next_space[0], next_space[1])
            if self.piece:
                nextgame.select(self.piece)

            child_node = Node(parent=self, game=nextgame, piece=next_piece)
            self.children.append(child_node)
            self.actions.remove(next_action)
            return child_node

    def best_child(self):  # chooses most visited (aka most successful) child
        best_child = None
        if self.children:
            random.shuffle(self.children)
            best_child = max(self.children, key=lambda child: child.stats[1])
        return best_child

    def best_uct(self):  # chooses child with highest UCT score
        parent_visits = self.stats[1]
        best_utc_child = self

        if self.children:
            best_utc_child = self.children[0]
            for child in self.children:
                child.score = calculate_uct(child.stats[1], child.stats[0], parent_visits)
                if child.score > best_utc_child.score:
                    best_utc_child = child

        return best_utc_child
