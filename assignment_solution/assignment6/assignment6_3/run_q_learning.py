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

from assignment_solution.assignment6.assignment6_3 import Maze
import matplotlib.pylab as plt
import pandas as pd
import os

from assignment_solution.assignment6.assignment6_3.RL_brain import QLearningTable

# logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                     filename='maze_q_learning.log',
#                     filemode='a',
#                     level=logging.DEBUG)
# logger = logging.getLogger()

# config
MAX_STEPS = 200
total_episodes = 600
save_episodes_interval = 100
output_dir = '../../../assignment_5/result/q_learning'
reward_file = 'reward.csv'


final_reward_lst = []
slidding_reward_lst = []
def update():
    for episode in range(total_episodes):
        # initial observation
        observation = env.reset()
        # print('episode',episode)
        R = []
        A = []
        step = 0
        # slidding_reward =
        while True:
            # fresh env
            env.render()
            step += 1
            # RL choose action based on observation
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            observation = observation_
            R.append(reward)
            A.append(action)
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
    # end of game
    print('game over')
    env.destroy()
    plt.plot(final_reward_lst)
    # plt.plot(slidding_reward_lst)
    plt.show()
    plt.savefig(os.path.join(output_dir, 'total_reward.png'))
    reward_df = pd.DataFrame({'total_reward': final_reward_lst})
    reward_df.to_csv(os.path.join(output_dir, reward_file))


if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))

    env.after(100, update)
    env.mainloop()