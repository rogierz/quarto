import numpy as np
from tqdm import trange
from quinto import quinto
from utils import parser, logger
from players import *
from contextlib import redirect_stdout


def benchmark(iterations=1000, actors=[RandomPlayer, MinmaxPlayer]):
    wins = np.zeros(3)
    stats = np.zeros(3)
    with redirect_stdout(None):
        with trange(iterations) as t:
            for i in t:
                t.set_postfix(
                    {"P0": f"{stats[0]:.2f}%", "P1": f"{stats[1]:.2f}%"})
                game = quinto.Quarto()
                players = list(map(lambda p: p(game), actors))
                game.set_players(players)
                winner = game.run()
                wins[winner] += 1
                stats = wins / (i + 1) * 100

    logger.info(f"Player 0 [{actors[0].__name__}] wins: {stats[0]:.2f}%")
    logger.info(f"Player 1 [{actors[1].__name__}] wins: {stats[1]:.2f}%")

    return stats


def tournament(tournament_name="all"):
    players_keys = [p for p in PLAYERS.keys() if p != 'random']
    players_indexes = list(range(len(players_keys)))
    results = np.zeros((len(players_keys), len(players_keys)))

    for p0 in players_indexes:
        for p1 in players_indexes:
            if p0 == p1:
                continue
            logger.info(f"{players_keys[p0]} vs {players_keys[p1]}")
            stats = benchmark(iterations=100, actors=[
                PLAYERS[players_keys[p0]], PLAYERS[players_keys[p1]]])
            results[p0, p1] = stats[0]

    results.tofile(f"{tournament_name}_tournament.npy")


def tournament_opponent_random(tournament_name="all_vs_random"):
    players_keys = [p for p in PLAYERS.keys() if p != 'random']
    players_indexes = list(range(len(players_keys)))
    results = np.zeros((len(players_keys), 2))

    for p0 in players_indexes:
        logger.info(f"{players_keys[p0]} vs random")
        stats = benchmark(iterations=100, actors=[
            PLAYERS[players_keys[p0]], PLAYERS['random']])
        results[p0, 0] = stats[0]
        logger.info(f"random vs {players_keys[p0]}")
        stats = benchmark(iterations=100, actors=[
            PLAYERS['random'], PLAYERS[players_keys[p0]]])
        results[p0, 1] = stats[1]
    np.save(f"{tournament_name}_tournament.npy", results)


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
    elif args.tournament:
        tournament()
    elif args.tournament_against_random:
        tournament_opponent_random()
    else:
        main(args.p0, args.p1)
