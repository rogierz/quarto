import random
from quinto import quinto
from .base import BasePlayer
from copy import deepcopy
import numpy as np
from collections import defaultdict
import pickle


def default_init():
    return 0


class RLPlayer(BasePlayer):

    def __init__(
            self,
            quarto: quinto.Quarto,
            train=False,
            alpha=0.15,
            random_factor=0.2) -> None:
        super().__init__(quarto)
        self.train = train
        self.state_history = []  # state, reward
        self.alpha = alpha
        self.gamma = 1
        self.random_factor = random_factor
        if self.train:
            self.Q = defaultdict(default_init)
        else:
            self.load_model()

        self.next_piece = None
        self.episode_reward = 0

    def update_episode_reward(self, new_reward):
        self.episode_reward += new_reward

    def choose_piece(self) -> int:
        if self.next_piece is None and self.train:
            # initialization
            action = self.choose_action()
            state, reward = self.get_state_and_reward(action)
            self.update_state_history(state, reward)
            self.update_episode_reward(reward)
            return action[0]
        if self.next_piece is None and not self.train:
            # read from the Q table
            best_action = self.best_action()
            return best_action[0]

        return self.next_piece

    def place_piece(self) -> tuple[int, int]:
        if self.train:
            action = self.choose_action()
            state, reward = self.get_state_and_reward(action)
            self.update_state_history(state, reward)
            self.update_episode_reward(reward)
            self.next_piece = action[0]
            return action[1][0], action[1][1]

        best_action = self.best_action()
        self.next_piece = best_action[0]
        return best_action[1][0], best_action[1][1]

    def choose_action(self):
        maxG = -10e15
        next_move = None
        randomN = np.random.random()
        allowed_action = self._game.available_actions
        if randomN < self.random_factor:
            # if random number below random factor, choose random action
            # chosen piece, position to place current piece
            next_move = random.choice(allowed_action)
            next_move = next_move[0], next_move[1]
        else:
            # if exploiting, gather all possible actions and choose one with
            # the highest G (reward)
            for action in allowed_action:
                board_state = (str(self._game.get_board_status()),
                               self._game.get_selected_piece())
                next_action = (action[0], action[1])

                if self.Q[board_state, next_action] >= maxG:
                    next_move = next_action
                    maxG = self.Q[board_state, next_action]

        return next_move

    def best_action(self):
        board_state = (str(self._game.get_board_status()),
                       self._game.get_selected_piece())
        max = float('-inf')
        next_action = None
        for action in self._game.available_actions:
            action_try = (action[0], action[1])
            local_max = self.Q[board_state, action_try]
            if local_max > max:
                max = local_max
                next_action = action_try

        return next_action

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        max_state_history = max(self.state_history, key=lambda x: x[1])[1]
        for prev, reward in reversed(self.state_history):

            adjusted_reward = reward + self.gamma * max_state_history
            self.Q[prev] = self.Q[prev] + self.alpha * \
                (adjusted_reward - self.Q[prev])

        self.state_history = []

        self.random_factor -= 10e-5  # decrease random factor each episode of play

    def get_state_and_reward(self, action):
        reward = -1
        sim_quarto = self.get_game()
        sim_quarto.place(action[1][0], action[1][1])
        if sim_quarto.check_winner() >= 0:
            reward = 100 if self._game.get_current_player() == self.moving_index else -100
        elif sim_quarto.check_finished():
            reward = -100
        prev_state = (str(self._game.get_board_status()),
                      self._game.get_selected_piece()), action
        return prev_state, reward

    def reset_player(self):
        self.episode_reward = 0
        self.next_piece = None

    def save_model(self):
        with open('./agents/rl_agent.pickle', 'wb') as f:
            pickle.dump(self.Q, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_model(self):
        with open('./agents/rl_agent.pickle', 'rb') as f:
            self.Q = pickle.load(f)

    def __deepcopy__(self, memo):
        cls = self.__class__
        obj = cls.__new__(cls)
        memo[id(self)] = obj
        for k, v in self.__dict__.items():
            if k in ['Q']:
                v = None
            setattr(obj, k, deepcopy(v, memo))
            pass
        return obj
