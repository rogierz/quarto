from quinto.quinto import Quarto
from players import *
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
from tqdm import trange
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', choices=['naive', 'minmax', 'random', 'risky', 'montecarlo'],
                        help='selects opponent player', required=True)
    parser.add_argument('-of', action='store_true', help='set if opponent is thr first player', required=False)
    args = parser.parse_args()
    game = Quarto()
    player_rl = RLPlayer(game, train=True)
    player_opponent = PLAYERS[args.o](game)

    players = (player_opponent, player_rl) if args.of else (player_rl, player_opponent)
    index_rl_player = 0 if isinstance(players[0], RLPlayer) else 1
    game.set_players(players)
    rewards_per_episode = []
    iterations = 2000
    with redirect_stdout(None):
        with trange(iterations) as t:
            for i in t:
                winner = game.run()
                players[index_rl_player].learn()
                rewards_per_episode.append(players[index_rl_player].episode_reward)
                game.reset_all()
                players[index_rl_player].reset_player()
                game.set_players(players)
        players[index_rl_player].save_model()

    min_reward = abs(min(rewards_per_episode)) + 10e-4
    fixed_reward = [elm + min_reward for elm in rewards_per_episode]
    plt.figure()
    plt.semilogy(fixed_reward)
    plt.savefig('./images/reward_per_episode.png')
