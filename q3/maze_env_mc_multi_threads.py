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
import concurrent.futures
import matplotlib.pylab as plt
import sys
from tqdm import tqdm
from copy import deepcopy
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

from maze_env import Maze


import logging
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename='maze_mc.log',
                    filemode='a',
                    level=logging.DEBUG)
logger = logging.getLogger()


def simulation():
    R = [-1]
    A = []
    max_teps = 10000
    env = Maze()
    step = 0
    np.random.seed()
    state_lst = [[0, 0]]
    while True:
        # env.render()
        step += 1
        a = np.random.choice([0, 1, 2, 3])
        s, r, done = env.step(a)
        R.append(r)
        if r == -50:
            state_lst.append([5, 6])
        elif r == 50:
            state_lst.append([8, 8])
        else:
            state = [int(s[-2] / 40 - 1), int(s[-1] / 40 - 1)]
            state_lst.append(state)
        if done or step > max_teps:
            break
    env.destroy()
    time_table = np.zeros((9, 9))
    reward_table = np.zeros((9, 9))
    total_reward = 0
    for idx in range(len(R)-1, -1, -1):
        reward = R[idx]
        state = state_lst[idx]
        i, j = state
        total_reward += reward
        if state not in state_lst[:idx]:
            reward_table[j][i] += total_reward
            time_table[j][i] += 1

    # # return sum(R), step
    # return state_lst, R
    return reward_table, time_table
    # total_rewards_lst.append(sum(R))
    # total_steps_lst.append(step)

def update(multi=False):
    # config
    debug = False
    output_dir = '../logs/mc_multi_threads'
    similation_num = 10000
    if debug:
        similation_num = 3
    # s_table = np.zeros((9,9))
    total_reward = np.zeros((9, 9))
    total_time = np.zeros((9, 9))
    basic_env = Maze()
    # for i in tqdm(range(dim)):
    #     for j in range(dim):
    #         if [i,j] in basic_env.wall:
    #             continue
    total_rewards_lst = []
    total_steps_lst = []
    if multi:
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(simulation) for _ in range(similation_num)]
            for future in concurrent.futures.as_completed(futures):
                # print(future.result())
                # reward, time = future.result()
                reward_table, time_table = future.result()
                total_reward += reward_table
                total_time += time_table


                # total_rewards_lst.append(R)
                # total_steps_lst.append(step)
    else:
        for t in tqdm(range(similation_num)):
            reward_table, time_table = simulation()
            total_reward += reward_table
            total_time += time_table


    print(total_reward)
    print(total_time)
    s_table = pd.DataFrame(total_reward/total_time)
    s_table = s_table.fillna(0)
    # plt.figure()
    plt.figure()
    sns.heatmap(s_table)
    print('Saving image...')
    plt.savefig(os.path.join(output_dir, 'heatmap.png'))
    # plt.show()
    print('Saving data..')
    pd.DataFrame(s_table).to_csv(os.path.join(output_dir, 'mc_result.csv'))
    pd.DataFrame(total_reward).to_csv(os.path.join(output_dir, 'total_reward.csv'))
    pd.DataFrame(total_time).to_csv(os.path.join(output_dir, 'first_visited_time.csv'))


if __name__ == '__main__':
    multi = False
    import time
    begin = time.time()
    # env = Maze()
    update(multi=multi)
    end = time.time()
    duration = end - begin
    print(duration)

    """
    # time
    2. new sequential 14.39
    3. multi-processes: 
        processor: 8.83
        thread: 
    """
