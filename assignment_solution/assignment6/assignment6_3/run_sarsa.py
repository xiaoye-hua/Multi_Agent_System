"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the main part which controls the update method of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
import matplotlib.pylab as plt
import os
import pandas as pd

from assignment_solution.assignment6.assignment6_3 import Maze
from assignment_solution.assignment6.assignment6_3.RL_brain import SarsaTable

def update():
    # config
    MAX_STEPS = 200
    total_episodes = 600
    save_episodes_interval = 100
    output_dir = '../../../assignment_5/result/sarsa'
    reward_file = 'reward.csv'

    final_reward_lst = []
    for episode in range(total_episodes):
        # initial observation
        observation = env.reset()

        # RL choose action based on observation
        action = RL.choose_action(str(observation))
        step = 0
        R = []
        while True:
            # fresh env
            env.render()
            step += 1
            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            # RL choose action based on next observation
            action_ = RL.choose_action(str(observation_))

            # RL learn from this transition (s, a, r, s, a) ==> Sarsa

            RL.learn(str(observation), action, reward, str(observation_), action_)
            # swap observation and action
            observation = observation_
            action = action_

            R.append(reward)
            total_reward = sum(R)

            # break while loop when end of this episode
            if done or step>MAX_STEPS:
                print(R)
                # slidding_reward = slidding_reward * 0.99 + total_reward * 0.01
                print(f"Episode: {episode}; total steps: {step}; final reward: {reward}; total reward: {total_reward};"
                      # f" slidding reward: {slidding_reward}"
                      )
                final_reward_lst.append(total_reward)
                # slidding_reward_lst.append(slidding_reward)

            if done:
                break
            if step>MAX_STEPS:
                break
        if episode == total_episodes-1 or episode%save_episodes_interval == 0:
            if episode == total_episodes-1:
                file_name = f"q_table_final.csv"
            else:
                file_name = f"q_table_{episode}.csv"
            RL.q_table.to_csv(os.path.join(output_dir, file_name))
    print('game over')
    env.destroy()
    plt.plot(final_reward_lst)
    # plt.plot(slidding_reward_lst)
    plt.savefig(os.path.join(output_dir, 'total_reward.png'))
    reward_df = pd.DataFrame({'total_reward': final_reward_lst})
    reward_df.to_csv(os.path.join(output_dir, reward_file))

if __name__ == "__main__":
    env = Maze()
    # RL = QLearningTable(actions=list(range(env.n_actions)))
    RL = SarsaTable(actions=list(range(env.n_actions)))

    env.after(100, update)
    env.mainloop()