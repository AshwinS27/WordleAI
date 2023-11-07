import gymnasium as gym
import numpy as np
import gym_wordle
from gym_wordle.exceptions import InvalidWordException
import random

print(gym.envs.registry.keys())

env = gym.make('Wordle-v0')
# obs = env.reset()
# act = env.action_space.sample()
# obs, reward, done, _ = env.step(act)
# env.render()

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

q_table = np.zeros([env.observation_space.n, env.action_space.n])
print(q_table.shape)

# For plotting metrics
all_epochs = []
all_penalties = []

for i in range(1, 100001):
    state = env.reset()

    epochs, penalties, reward, = 0, 0, 0
    done = False


    while not done:
        while True:
            try:
                #act = "hello"
                # make a random guess
                if random.uniform(0, 1) < epsilon:
                    action = env.action_space.sample() # Explore action space
                else:
                    action = np.argmax(q_table[state]) # Exploit learned values
                # take a step
                next_state, reward, done, info = env.step(action)
                print("Reward: ", reward)

                old_value = q_table[state, action]
                next_max = np.max(q_table[next_state])
                
                new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
                q_table[state, action] = new_value

                if reward == -10:
                    penalties += 1

                state = next_state
                epochs += 1
                break
            except InvalidWordException:
                pass
        env.render()