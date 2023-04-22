import random
import numpy as np
import pickle
import os
from quinto import quinto
from .base import BasePlayer
from .random import RandomPlayer
from collections import namedtuple
from copy import deepcopy
ParamsBase = namedtuple("ParamsBase", "aggressive, defensive, mood")
MU = 0
SIGMA = 0.1
MUTATION_RATE = 0.3

FILE_NAME= "evolved.pkl"
FILE_PATH = os.path.join("agents", FILE_NAME)

class PlayerParams(ParamsBase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mu = np.zeros(len(self))
        self.sigma = np.ones(len(self))*0.1
        self._fitness = None

    def __invert__(self):
        new_self = self
        if random.random() <= MUTATION_RATE:
            new_self = deepcopy(self)
            for i in len(new_self):
                new_self.mu += np.random.normal(MU, SIGMA, new_self.mu.shape)
                new_self.sigma += np.random.normal(MU, SIGMA, new_self.sigma.shape)
                new_self[i] += np.random.normal(new_self.mu[i], new_self.sigma[i])
                new_self[i] = np.clip(new_self[i], (0, 1))
        return new_self

    def __xor__(self, other):
        w = np.array([self.fitness, other.fitness])
        w = w / (self.fitness + other.fitness)
        new_born = PlayerParams(*[np.clip(self[i]*w[i] + other[i]*w[i], (0, 1)) for i in range(len(self))])
        return new_born

    @property
    def fitness(self, games=100):
        if self._fitness is None:
            wins = np.zeros(3)
            for _ in range(games):
                game = quinto.Quarto()
                players = [EvolutionaryPlayer(game, self), RandomPlayer(game)]
                game.set_players(players)
                winner = game.run()
                wins[winner] +=1
            self._fitness = wins[0]/games*100
        return self._fitness

class EvolutionaryPlayer(BasePlayer):
    """Evolutionary player"""
    
    def __init__(self, quarto: quinto.Quarto, params=None) -> None:
        super().__init__(quarto)
        if params is None:
            with open(FILE_PATH, "r") as fs:
                self._params = pickle.load(fs)
        else:
            self._params = params
        
    def choose_piece(self) -> int:
        in_mood = random.random() <= self._params.mood
        if in_mood and random.random() <= self._params.aggressive:
            #play aggressive
            pass
        elif not in_mood and random.random() <= self._params.defensive:
            #play defensive
            pass
        else:
            piece = random.choice(self._game.available_pieces)
        return piece

    def place_piece(self) -> tuple[int, int]:
        in_mood = random.random() <= self._params.mood
        if in_mood and random.random() <= self._params.aggressive:
            #play aggressive
            pass
        elif not in_mood and random.random() <= self._params.defensive:
            #play defensive
            pass
        else:
            x, y = random.choice(self._game.available_position)
        return x, y