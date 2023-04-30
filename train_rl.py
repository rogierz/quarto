from quinto.quinto import Quarto
from players import *
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
from tqdm import trange
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        choices=[
            'naive',
            'minmax',
            'random',
            'risky',
            'montecarlo'],
        help='selects opponent player',
        required=True)
    parser.add_argument(
        '-of',
        action='store_true',
        help='set if opponent is thr first player',
        required=False)
    args = parser.parse_args()
    game = Quarto()
    player_rl = RLPlayer(game, train=True)
    player_opponent = PLAYERS[args.o](game)

    players = (
        player_opponent,
        player_rl) if args.of else (
        player_rl,
        player_opponent)
    index_rl_player = 0 if isinstance(players[0], RLPlayer) else 1
    game.set_players(players)
    rewards_per_episode = []
    iterations = 2000
    with redirect_stdout(None):
        with trange(iterations) as t:
            for i in t:
                winner = game.run()
                players[index_rl_player].learn()
                rewards_per_episode.append(
                    players[index_rl_player].episode_reward)
                game.reset_all()
                players[index_rl_player].reset_player()
                game.set_players(players)
        players[index_rl_player].save_model()

    average = []

    for i in range(len(rewards_per_episode)):
        episode_rew = rewards_per_episode[:i+1]
        average.append(sum(episode_rew) / (i + 1))

    plt.figure()
    plt.title("Average rewards")
    plt.plot(average)
    plt.savefig('./images/new_reward_per_episode.png')
