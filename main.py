from tqdm import trange
from quarto import quarto
from utils import parser, logger
from players import *
from contextlib import redirect_stdout

def benchmark(iterations=1000, actors=[RandomPlayer, MinmaxPlayer]):
    wins = [0, 0]
    with redirect_stdout(None):
        for i in trange(iterations):
            game = quarto.Quarto()
            players = list(map(lambda p: p(game), actors))
            game.set_players(players)
            winner = game.run()
            wins[winner] +=1

    stats = list(map(lambda x: x/iterations*100, wins))
    logger.info(f"Player 0 [{actors[0].__name__}] wins: {stats[0]:.2f}%")
    logger.info(f"Player 1 [{actors[1].__name__}] wins: {stats[1]:.2f}%")

    
def main(p0, p1):
    game = quarto.Quarto()
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
