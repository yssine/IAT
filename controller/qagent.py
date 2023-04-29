import os
import numpy as np
from epsilon_profile import EpsilonProfile
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

from game import SpaceInvaders

X_MIN = 0
X_MAX = 770
Y_MIN = 0
Y_MAX = 500

NUMER_ACTIONS = 4


class QAgent():
    def __init__(self,
                 spaceInvaders: SpaceInvaders,
                 eps_profile: EpsilonProfile,
                 gamma: float,
                 alpha: float,
                 fileLog="logQ"):
        self.na = NUMER_ACTIONS
        self.Q = np.zeros([X_MAX + 1, Y_MAX + 1, 1 + 1, self.na])
        self.spaceInvaders = spaceInvaders
        self.gamma = gamma
        self.alpha = alpha
        self.eps_profile = eps_profile
        self.epsilon = self.eps_profile.initial
        self.qvalues = pd.DataFrame(data={'episode': [], 'score': [], 'Q_sum': []})
        self.fileLog = fileLog

    def getQ(self, state, action):
        return self.Q[state[0]][state[1]][state[2]][action]

    def setQ(self, state, action, value):
        self.Q[state[0]][state[1]][state[2]][action] = value

    def saveQToFile(self,
                    file=os.path.join(os.path.dirname(__file__),
                                      '../LearnedQ/LearnedQ.npy')):
        np.save(file, self.Q)

    def loadQFromFile(self,
                      file=os.path.join(os.path.dirname(__file__),
                                        '../LearnedQ/LearnedQ.npy')):
        self.Q = np.load(file)

    def learn(self, env: SpaceInvaders, n_episodes, max_steps):
        n_steps = np.zeros(n_episodes) + max_steps
        for episode in range(n_episodes):
            state = env.reset()
            for step in range(max_steps):
                action = self.select_action(state)
                next_state, reward, terminal = env.step(action)
                self.updateQ(state, action, reward, next_state)
                if terminal:
                    n_steps[episode] = step + 1
                    break
                state = next_state
            self.epsilon = max(
                self.epsilon - self.eps_profile.dec_episode /
                (n_episodes - 1.), self.eps_profile.final)
            if n_episodes >= 0:
                print(f"\r#> Ep.: {episode}/{n_episodes-1}\tSum(Q): {np.sum(self.Q)}\tCurr. Score: {self.spaceInvaders.score_val}",end=" ")
                self.save_log(env, episode)
                state = env.reset()

        self.qvalues.to_csv(
            os.path.join(os.path.dirname(__file__), '../visualisation',
                         self.fileLog + '.csv'))

    def updateQ(self, state, action, reward, next_state):
        # If invader reached boarder its y-position is set to a too small value. This one has to be
        # increased to make it at least Y_MAX
        if next_state[1] < Y_MIN:
            next_state[1] = Y_MIN
        val = (1. - self.alpha) * self.getQ(state, action) + self.alpha * (
            reward + self.gamma * np.max(self.Q[next_state]))
        self.setQ(state, action, val)

    def select_action(self, state: int):

        if np.random.rand() < self.epsilon:
            a = np.random.randint(self.na)  # random action
        else:
            a = self.select_greedy_action(state)

        return a

    def select_greedy_action(self, state: 'Tuple[int, int]'):
        # If invader reached boarder its y-position is set to a too small value. This one has to be
        # increased to make it at least Y_MAX
        if state[1] < Y_MIN:
            state[1] = Y_MIN

        mx = np.max(self.Q[state])
        return np.random.choice(np.where(self.Q[state] == mx)[0])

    def save_log(self, env, episode):
        self.qvalues = self.qvalues.append(
            {
                'episode': episode,
                'score': self.spaceInvaders.score_val,
                'Q_sum': np.sum(self.Q)
            },
            ignore_index=True)
