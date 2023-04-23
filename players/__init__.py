from .naive import NaivePlayer
from .random import RandomPlayer
from .risky import RiskyPlayer
from .minmax import MinmaxPlayer
from .montecarlo import MonteCarloPlayer
from .rl import RLPlayer

PLAYERS = {
    'naive': NaivePlayer,
    'minmax': MinmaxPlayer,
    'random': RandomPlayer,
    'risky': RiskyPlayer,
    'montecarlo': MonteCarloPlayer,
    'rl': RLPlayer
}
