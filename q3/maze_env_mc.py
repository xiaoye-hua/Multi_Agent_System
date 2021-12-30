"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example. The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
import numpy as np
import time
import os
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import sys
from tqdm import tqdm
from copy import deepcopy
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

import logging
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename='maze_mc.log',
                    filemode='a',
                    level=logging.DEBUG)
logger = logging.getLogger()


UNIT = 1   # pixels
MAZE_H = 9  # grid height
MAZE_W = 9  # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self._build_maze()

    def _build_maze(self):
        self.canvas = np.ones((9,9))*(-1)

        # create grids
        # snakepit
        self.hell1 = [6,5]
        # treasure
        self.hell2 = [8,8]

        # create wall
        self.wall = [[1,2],[1,3],[1,4],[1,5],[1,6],[2,6],[3,6],[4,6],[5,6],[7,1],[7,2],[7,3],[7,4]]

        # # create red rect
        self.rect = [0,0]

        # pack all

    def reset(self):
        self.update()
        self.rect = [0,0]
        # return observation

    def step(self, action):
        s = deepcopy(self.rect)
        base_action = [0, 0]
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.rect = [self.rect[0]+base_action[0], self.rect[1]+base_action[1]]  # move agent

        s_ = self.rect  # next state

        # reward function
        if s_ in self.wall:
            self.rect = [self.rect[0]-base_action[0], self.rect[1]-base_action[1]]    # move back
            reward = -1
            done = False
            s_ = s
        elif s_ == self.hell1:
            reward = -50
            done = True
            s_ = 'terminal'
        elif s ==  self.hell2:
            reward = 50
            done = True
            s_ = 'terminal'
        else:
            reward = -1
            done = False

        return s_, reward, done

    def render(self):
        time.sleep(0.05)
        self.update()


def update():
    # config
    debug = False
    output_dir = '../logs/mc'
    similation_num = 10
    if debug:
        dim = 2
        similation_num = 1
    else:
        dim = 9
    max_teps = 200
    s_table = np.zeros((9,9))
    for i in tqdm(range(dim)):
        for j in range(dim):
            if [i,j] in env.wall:
                continue
            total_rewards_lst = []
            total_steps_lst = []
            for t in tqdm(range(similation_num)):
                R = []
                A = []
                s = env.reset()
                step = 0
                while True:
                    env.render()
                    step += 1
                    a = np.random.choice([0, 1, 2, 3])
                    s, r, done = env.step(a)
                    R.append(r)
                    A.append(a)
                    # print(env.rect)
                    if done or step>max_teps:
                        break
                # logger.info("R")
                # logger.info(R)
                # logger.info("A")
                # logger.info(A)
                total_rewards_lst.append(sum(R))
                total_steps_lst.append(step)
            # s_table[i][j] = s_table[i][j] + 1/(t+1)*(sum(R)-s_table[i][j])
            print(f"Position: [{i}, {j}]; simulation num: {similation_num}")
            print(f"    Reward statistic:"
                  f" mean:{np.mean(total_rewards_lst)}; max: {np.max(total_rewards_lst)}; min: {np.min(total_rewards_lst)}")
            s_table[i][j] = np.mean(total_rewards_lst)
            print(f"    Step statistic:"
                  f" mean:{np.mean(total_steps_lst)}; max: {np.max(total_steps_lst)}; min: {np.min(total_steps_lst)}")
            s_table[i][j] = np.mean(total_rewards_lst)
            plt.figure()
            sns.heatmap(s_table)
            print('Saving image...')
            plt.savefig(os.path.join(output_dir, f'heatmap_{i}_{j}.png'))
            # logger.info(s_table)
    plt.figure()
    sns.heatmap(s_table)
    print('Saving image...')
    plt.savefig(os.path.join(output_dir, 'heatmap.png'))
    # plt.show()
    print('Saving data..')
    pd.DataFrame(s_table).to_csv(os.path.join(output_dir, 'mc_result.csv'))




if __name__ == '__main__':
    env = Maze()
    env.after(10, update)
    env.mainloop()
