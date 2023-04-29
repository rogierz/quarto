import random
import numpy as np
import pickle
import os
from quinto import quinto
from .base import BasePlayer
from .random import RandomPlayer
from collections import namedtuple
from copy import deepcopy
MU = 0
SIGMA = 0.1
MUTATION_RATE = 0.3
FILE_NAME = "evolved_agent.pkl"
FILE_PATH = os.path.join("agents", FILE_NAME)


class PlayerParams(list):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mu = np.zeros(len(self))
        self.sigma = np.ones(len(self)) * 0.1
        self._fitness = None

    @property
    def aggressive(self):
        return self[0]

    @property
    def defensive(self):
        return self[1]

    @property
    def mood(self):
        return self[2]

    def __invert__(self):
        new_self = self
        if random.random() <= MUTATION_RATE:
            new_self = deepcopy(self)
            for i in range(len(new_self)):
                new_self.mu += np.random.normal(MU, SIGMA, new_self.mu.shape)
                new_self.sigma += np.random.normal(MU,
                                                   SIGMA, new_self.sigma.shape)
                new_self.sigma[new_self.sigma < 0] = 1e-4
                new_self[i] = new_self[i] + \
                    np.random.normal(new_self.mu[i], new_self.sigma[i])
                new_self[i] = np.clip(new_self[i], 0, 1)
        return new_self

    def __xor__(self, other):
        w = np.array([self.fitness, other.fitness])
        w = w / (self.fitness + other.fitness)
        new_born = PlayerParams(
            [np.clip(self[i] * w[0] + other[i] * w[1], 0, 1).ravel() for i in range(len(self))])
        return new_born

    @property
    def fitness(self, games=10):
        if self._fitness is None:
            wins = np.zeros(3)
            for _ in range(games):
                game = quinto.Quarto()
                players = [EvolutionaryPlayer(game, self), RandomPlayer(game)]
                game.set_players(players)
                winner = game.run()
                wins[winner] += 1
            self._fitness = wins[0] / games * 100
        return self._fitness


class EvolutionaryPlayer(BasePlayer):
    """Evolutionary player"""

    def __init__(self, quarto: quinto.Quarto, params=None) -> None:
        super().__init__(quarto)
        if params is None:
            with open(FILE_PATH, "rb") as fs:
                self._params = pickle.load(fs)
        else:
            self._params = params

    def cook_status(self):
        status = {}
        pieces_counter = np.zeros((4, 2))
        available_pieces = deepcopy(self._game.available_pieces)
        winning_position_opponent = self._list_winning_positions()
        if len(winning_position_opponent) > 0:
            # if there is a winning position for the opponent then delete the
            # pieces that makes them winning
            for position in winning_position_opponent:
                for piece in available_pieces:
                    winner = self._simulate_winning_move(position, piece)
                    if winner:
                        available_pieces.remove(piece)

        status['available_pieces'] = available_pieces

        status['winning_moves'] = []
        candidate_winning_position = self._list_winning_positions()
        if len(candidate_winning_position) > 0:
            for position in candidate_winning_position:
                winner = self._simulate_winning_move(position)
                if winner:
                    status['winning_moves'].append(position)

        for piece in available_pieces:
            piece_traits = list(
                map(lambda i: int(piece & (1 << i) == (1 << i)), [0, 1, 2, 3]))
            pieces_counter[np.arange(4), piece_traits] += 1

        status['piece_counter'] = pieces_counter

        indexes_not_empty = self._game._board != -1
        row_counter = indexes_not_empty.sum(axis=0)
        col_counter = indexes_not_empty.sum(axis=1)
        diags_counter = np.array(
            [indexes_not_empty.trace(), np.fliplr(indexes_not_empty).trace()])

        status['length_counter'] = (row_counter, col_counter, diags_counter)

        row_stats = np.empty((4, 4, 2))
        col_stats = np.empty((4, 4, 2))
        diag_stats = np.empty((2, 4, 2))

        for i in range(4):
            row_stats[i] = self._reduce_array(self._game._board[i, :])
            col_stats[i] = self._reduce_array(self._game._board[:, i])

        diag_stats[0] = self._reduce_array(self._game._board.diagonal())
        diag_stats[1] = self._reduce_array(
            np.fliplr(self._game._board).diagonal())

        status['board_counter'] = (row_stats, col_stats, diag_stats)

        return status

    def _reduce_array(self, array):
        array = array.reshape((4,))
        result = np.zeros((4, 2))
        for elem in array:
            if elem == -1:
                continue
            piece_traits = list(
                map(lambda i: int(elem & (1 << i) == (1 << i)), [0, 1, 2, 3]))
            result[np.arange(4), piece_traits] += 1
        return result

    def choose_piece(self) -> int:
        status = self.cook_status()
        length_status = status['length_counter']
        max_length = max(
            length_status[0].max(),
            length_status[1].max(),
            length_status[2].max())
        for i, dim in enumerate(length_status):
            if max_length in dim:
                dim_index = np.where(dim == max_length)[0][0]
                if i == 0:
                    extracted_dim = self._game._board[dim_index, :]
                elif i == 1:
                    extracted_dim = self._game._board[:, dim_index]
                elif i == 2:
                    extracted_dim = self._game._board.diagonal(
                    ) if dim_index == 0 else np.fliplr(self._game._board).diagonal()
                break

        piece = random.choice(self._game.available_pieces)
        if (extracted_dim != -1).any():
            dim_stats = self._reduce_array(extracted_dim)
            max_values = np.where(dim_stats == dim_stats.max())
            bit_index, bit_value = max_values[0][0], max_values[1][0]
            bit_value = 1 - bit_value
            bit_mask = 1 << bit_index
            bit_filter = bit_value << bit_index
            good_choices = list(filter(lambda x: (
                ~((x & bit_mask) ^ bit_filter) & bit_mask) == bit_mask, status['available_pieces']))
            if len(good_choices) > 0:
                piece = good_choices[0]

        if piece not in self._game.available_pieces:
            piece = random.choice(self._game.available_pieces)
        return piece

    def place_piece(self) -> tuple[int, int]:
        in_mood = random.random() <= self._params.mood
        position = random.choice(self._game.available_position)
        status = self.cook_status()
        if len(status['winning_moves']) > 0:
            return status['winning_moves'][0]

        length_status = status['length_counter']

        if in_mood and random.random() <= self._params.aggressive:
            obj_length = max(
                length_status[0].max(),
                length_status[1].max(),
                length_status[2].max())
        elif not in_mood and random.random() <= self._params.defensive:
            obj_length = min(
                length_status[0].min(),
                length_status[1].min(),
                length_status[2].min())
        else:
            return position

        if obj_length == 0:
            return position

        for i, dim in enumerate(length_status):
            if obj_length in dim:
                dim_index = np.where(dim == obj_length)[0][0]
                if i == 0:
                    extracted_dim = self._game._board[dim_index, :].ravel()
                    if (extracted_dim != -1).all():
                        continue
                    position = np.where(extracted_dim == -1)[0][0], dim_index
                elif i == 1:
                    extracted_dim = self._game._board[:, dim_index].ravel()
                    if (extracted_dim != -1).all():
                        continue
                    position = dim_index, np.where(extracted_dim == -1)[0][0]
                elif i == 2:
                    extracted_dim = self._game._board.diagonal(
                    ) if dim_index == 0 else np.fliplr(self._game._board).diagonal()
                    extracted_dim = extracted_dim.ravel()
                    if (extracted_dim != -1).all():
                        continue
                    index = np.where(extracted_dim == -1)[0][0]
                    index = index
                    anti_index = index if dim_index == 0 else 3 - index
                    position = anti_index, index
                break

        if position not in self._game.available_position:
            return random.choice(self._game.available_position)
        return position
