from time import sleep
import random
import numpy as np
from environment import frozen_lake_v1
from environment import frozen_lake_v2
#version 1 prints
#version 2 makes a screen

env = frozen_lake_v2()
env.reset()

n_states = env.rows * env.columns
n_actions = env.actions
qtable = np.zeros((n_states, n_actions))

total_episode = 1
total_test_episode = 10
max_steps = 100

learning_rate = 0.7
gamma = 0.618

epsilon = 1.0
max_epsilon = 1.0
min_epsilon = 0.01
decay_rate = 0.01

total_reward = 0

for episode in range(total_episode):
    print('\repisode : ' + str(episode + 1), total_reward, end = '')
    total_reward = 0
    env.reset()
    state = env.possible[random.randint(0, len(env.possible) - 1)]
    step = 0
    done = False
    for step in range(max_steps):
        exp_exp_tradeoff = np.random.uniform(0, 1)
        if exp_exp_tradeoff > epsilon:
            action = np.argmax(qtable[int(state),:])

        else:
            action = random.randint(0, n_actions - 1)
        new_state, reward, done = env.step(action)
        qtable[state, action] = qtable[state, action] + learning_rate * (reward + gamma * np.max(qtable[new_state, :]) - qtable[state, action])
        total_reward += reward

        state = new_state
        if done == True:
            break
        episode += 1
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

print()
state = env.reset()
rewards = []
steps = []

for episode in range(total_test_episode):
    env.reset()
    done = False
    total_reward = 0
    s = []
    print('*********************************************************')
    print('Episode : ', episode)
    for step in range(max_steps):
        action = np.argmax(qtable[int(state),:])
        new_state, reward, done = env.step(action)

        total_reward += reward
        if done == True:
            s.append(new_state)
            env.render()
            rewards.append(total_reward)
            print('score :', total_reward)
            break
        state = new_state
        env.render()
        s.append( state )
    if done == False:
        rewards.append( total_reward )
        print( 'socre :', total_reward )
    steps.append(s)
print('final_scores = ', rewards, '  |   total = ', len(rewards))
print(steps[rewards.index(max(rewards))])
env.render_plot(steps[rewards.index(max(rewards))])
env.policy(qtable)

print(qtable)

