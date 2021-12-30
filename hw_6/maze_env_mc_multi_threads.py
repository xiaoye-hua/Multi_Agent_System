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





# UNIT = 1   # pixels
# MAZE_H = 9  # grid height
# MAZE_W = 9  # grid width


# class Maze(tk.Tk, object):
#     def __init__(self):
#         super(Maze, self).__init__()
#         self.action_space = ['u', 'd', 'l', 'r']
#         self.n_actions = len(self.action_space)
#         self._build_maze()
#
#     def _build_maze(self):
#         self.canvas = np.ones((9,9))*(-1)
#
#         # create grids
#         # snakepit
#         self.hell1 = [6,5]
#         # treasure
#         self.hell2 = [8,8]
#
#         # create wall
#         self.wall = [[1,2],[1,3],[1,4],[1,5],[1,6],[2,6],[3,6],[4,6],[5,6],[7,1],[7,2],[7,3],[7,4]]
#
#         # # create red rect
#         self.rect = [0,0]
#
#         # pack all
#
#     def reset(self):
#         self.update()
#         self.rect = [0,0]
#         # return observation
#
#     def step(self, action):
#         s = deepcopy(self.rect)
#         base_action = [0, 0]
#         if action == 0:   # up
#             if s[1] > UNIT:
#                 base_action[1] -= UNIT
#         elif action == 1:   # down
#             if s[1] < (MAZE_H - 1) * UNIT:
#                 base_action[1] += UNIT
#         elif action == 2:   # right
#             if s[0] < (MAZE_W - 1) * UNIT:
#                 base_action[0] += UNIT
#         elif action == 3:   # left
#             if s[0] > UNIT:
#                 base_action[0] -= UNIT
#
#         self.rect = [self.rect[0]+base_action[0], self.rect[1]+base_action[1]]  # move agent
#
#         s_ = self.rect  # next state
#
#         # reward function
#         if s_ in self.wall:
#             self.rect = [self.rect[0]-base_action[0], self.rect[1]-base_action[1]]    # move back
#             reward = -1
#             done = False
#             s_ = s
#         elif s_ == self.hell1:
#             reward = -50
#             done = True
#             s_ = 'terminal'
#         elif s ==  self.hell2:
#             reward = 50
#             done = True
#             s_ = 'terminal'
#         else:
#             reward = -1
#             done = False
#
#         return s_, reward, done
#
#     def render(self):
#         time.sleep(0.05)
#         self.update()

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
        # print(f"state: {state}")
        # print(state_lst)
        # print(R)
        # print()
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

            # R = []
            # A = []
            # # s = env.reset()
            # env = Maze()
            # step = 0
            # while True:
            #     step += 1
            #     a = np.random.choice([0, 1, 2, 3])
            #     s, r, done = env.step(a)
            #     R.append(r)
            #     A.append(a)
            #     if done or step>max_teps:
            #         break

            # R, step = simulation()
            # total_rewards_lst.append(R)
            # total_steps_lst.append(step)

    # print(f"Position: [{i}, {j}]; simulation num: {similation_num}")
    # print(f"    Reward statistic:"
    #       f" mean:{np.mean(total_rewards_lst)}; max: {np.max(total_rewards_lst)}; min: {np.min(total_rewards_lst)}")
    # s_table[i][j] = np.mean(total_rewards_lst)
    # print(f"    Step statistic:"
    #       f" mean:{np.mean(total_steps_lst)}; max: {np.max(total_steps_lst)}; min: {np.min(total_steps_lst)}")
    # s_table[i][j] = np.mean(total_rewards_lst)
    print(total_reward)
    print(total_time)
    s_table = pd.DataFrame(total_reward/total_time)
    s_table = s_table.fillna(0)
    # plt.figure()
    # sns.heatmap(s_table)
    # print('Saving image...')
    # # plt.savefig(os.path.join(output_dir, f'heatmap_{i}_{j}.png'))
    # # logger.info(s_table)
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

    # import concurrent.futures
    # import time
    # #
    # number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #
    #
    # def evaluate_item(x):
    #     # 计算总和，这里只是为了消耗时间
    #     result_item = count(x)
    #     # 打印输入和输出结果
    #     return 1
    #
    #
    # def count(number):
    #     for i in range(0, 10000000):
    #         i = i + 1
    #     return i * number
    #
    #
    # # 顺序执行
    # start_time = time.time()
    # for item in number_list:
    #     print(evaluate_item(item))
    # print("Sequential execution in " + str(time.time() - start_time), "seconds")
    # # 线程池执行
    # start_time_1 = time.time()
    # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #     futures = [executor.submit(evaluate_item, item) for item in number_list]
    #     for future in concurrent.futures.as_completed(futures):
    #         print(future.result())
    # print("Thread pool execution in " + str(time.time() - start_time_1), "seconds")
    # # 进程池
    # start_time_2 = time.time()
    # with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
    #     futures = [executor.submit(evaluate_item, item) for item in number_list]
    #     for future in concurrent.futures.as_completed(futures):
    #         print(future.result())
    # print("Process pool execution in " + str(time.time() - start_time_2), "seconds")
