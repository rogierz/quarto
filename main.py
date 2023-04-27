import numpy as np
from tqdm import trange
from quinto import quinto
from utils import parser, logger
from players import *
from contextlib import redirect_stdout


def benchmark(iterations=1000, actors=[RandomPlayer, MinmaxPlayer]):
    wins = np.zeros(2)
    stats = np.zeros(2)
    with redirect_stdout(None):
        with trange(iterations) as t:
            for i in t:
                t.set_postfix({"P0": f"{stats[0]:.2f}%", "P1": f"{stats[1]:.2f}%"})
                game = quinto.Quarto()
                players = list(map(lambda p: p(game), actors))
                game.set_players(players)
                winner = game.run()
                wins[winner] += 1
                stats = wins / (i + 1) * 100

    logger.info(f"Player 0 [{actors[0].__name__}] wins: {stats[0]:.2f}%")
    logger.info(f"Player 1 [{actors[1].__name__}] wins: {stats[1]:.2f}%")


def main(p0, p1):
    game = quinto.Quarto()
    players = (p0(game), p1(game))
    game.set_players(players)
    winner = game.run()
    logger.warning(f"main: Winner: player {winner} [{players[winner]}]")


if __name__ == '__main__':
    args = parser.parse_args()
    args.p0 = PLAYERS[args.p0]
    args.p1 = PLAYERS[args.p1]
    logger = logger.configureLogger(args)
    if args.benchmark:
        benchmark(actors=[args.p0, args.p1])
    else:
        main(args.p0, args.p1)
