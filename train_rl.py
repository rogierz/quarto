from quinto.quinto import Quarto
from players.rl import RLPlayer
from players.random import RandomPlayer
from players.risky import RiskyPlayer
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
from tqdm import trange

if __name__ == "__main__":

    game = Quarto()
    players = (RLPlayer(game, train=True), RandomPlayer(game))
    game.set_players(players)
    rewards_per_episode = []
    iterations = 50
    with redirect_stdout(None):
        with trange(iterations) as t:
            for i in t:
                winner = game.run()
                players[0].learn()
                rewards_per_episode.append(players[0].episode_reward)
                game.reset_all()
                players[0].reset_player()
                game.set_players(players)
        players[0].save_model()

    min_reward = abs(min(rewards_per_episode)) + 10e-4
    fixed_reward = [elm + min_reward for elm in rewards_per_episode]
    plt.figure()
    plt.semilogy(fixed_reward)
    plt.savefig('./images/reward_per_episode.png')
