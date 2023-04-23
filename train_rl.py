from quinto.quinto import Quarto
from players.rl import RLPlayer
from players.random import RandomPlayer
import matplotlib.pyplot as plt
from contextlib import redirect_stdout

if __name__ == "__main__":

    game = Quarto()
    players = (RLPlayer(game, moving_first=True, train=True), RandomPlayer(game))
    game.set_players(players)
    rewards_per_episode = []
    with redirect_stdout(None):
        for i in range(200):
            winner = game.run()
            players[0].learn()
            rewards_per_episode.append(players[0].episode_reward)
            game.reset_all()
            players[0].reset_player()
            game.set_players(players)
        players[0].save_model()

    plt.figure(2)
    plt.plot(rewards_per_episode)
    plt.show()
