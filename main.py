from quarto import quarto
from players.random import RandomPlayer
from players.naive import NaivePlayer
from players.risky import RiskyPlayer
from utils import parser, logger

def main():
    game = quarto.Quarto()
    players = (NaivePlayer(game), RiskyPlayer(game))
    game.set_players(players)
    winner = game.run()
    logger.warning(f"main: Winner: player {winner} [{players[winner]}]")


if __name__ == '__main__':
    args = parser.parse_args()
    logger = logger.configureLogger(args)
    main()
