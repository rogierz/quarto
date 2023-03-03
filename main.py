from quarto import quarto
from players.random import RandomPlayer
from players.naive import NaivePlayer
from players.risky import RiskyPlayer
from utils import parser, logger

def main():
    game = quarto.Quarto()
    game.set_players((NaivePlayer(game), RandomPlayer(game)))
    winner = game.run()
    logger.warning(f"main: Winner: player {winner}")


if __name__ == '__main__':
    args = parser.parse_args()
    logger = logger.configureLogger(args)
    main()
    logger.info("Logging an info")
