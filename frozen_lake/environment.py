from plot import Environment
from termcolor import colored
import pygame as pg
import numpy as np
import random

rows = 4
columns = 4
rewards = {'g' : 100000, 'f' : -100, 'w' : -1, 'b' : 0, '_' : -1}
oppisite_rewards = {}
for i in rewards:
    oppisite_rewards[rewards[i]] = i

class frozen_lake_v1:
    def __init__(self):
        self.rewards = rewards
        self.columns = columns
        self.rows = rows
        self.fire = []
        self.water = []
        self.brick = []
        self.start = 0
        self.end = 0
        self.slip = 0.33
        self.actions = 4
        self.get_inputs()
        self.state = self.start


    def reset(self):
        self.state = self.start
        return self.state

    def get_inputs(self):
        self.rows = int(input())
        self.columns = int(input())
        possible = []
        for i in range(self.rows):
            a = input().split()
            for j in range(self.columns):
                if a[j] == 'f':
                    self.fire.append(i * self.columns + j)
                elif a[j] == 'w':
                    self.water.append(i * self.columns + j)
                elif a[j] == 'b':
                    self.brick.append(i * self.columns + j)
                elif a[j] == 's':
                    self.start = i * self.columns + j
                    possible.append(int( (i * self.columns) + j))
                elif a[j] == 'g':
                    self.end = i * self.columns + j
                else:
                    possible.append( int( (i * self.columns) + j ) )
        self.possible = possible

    def move(self, action):
        s = self.state
        if action == 0:
            if self.state >= self.columns:
                self.state -= self.columns
        elif action == 1:
            if self.state + self.columns <= self.columns * self.rows - 1:
                self.state += self.columns
        elif action == 2:
            if self.state % 4 != 0:
                self.state -= 1
        else:
            if self.state % 4 != 3:
                self.state += 1
        done = False
        if self.state == self.end:
            done = True
        elif self.state in self.fire:
            done = True
        if self.state in self.brick:
            self.state = s
        return self.state, self.reward(), done


    def reward(self):
        for i in range(len(self.fire)):
            if self.state == self.fire[i]:
                return self.rewards['f']
        for i in range(
                len(self.brick)):
            if self.state == self.brick[i]:
                return self.rewards['b']
        for i in range(len(self.water)):
            if self.state == self.water[i]:
                return self.rewards['w']
        if self.state == self.end:
            return self.rewards['g']
        return self.rewards['_']

    def reward_for_certain_state(self, state):
        for i in range(len(self.fire)):
            if state == self.fire[i]:
                return colored('🔥', 'red')
        for i in range(len(self.brick)):
            if state == self.brick[i]:
                return colored('🧱', 'red')
        for i in range(len(self.water)):
            if state == self.water[i]:
                return colored('💧', 'blue')
        if state == self.end:
            return colored('🏁', 'green')
        if state == self.start:
            return colored('⚐', 'white')
        return '_'


    def step(self, action):
        rand = random.random()
        if rand < 1 - (self.slip * 2):
            a = 0
        elif rand < 1 - self.slip:
            a = 1
        else:
            a = 2
        if action == 0:
            b = [0, 2, 3]
            return self.move(b[a])
        elif action == 1:
            b = [1, 3, 2]
            return self.move(b[a])
        elif action == 2:
            b = [2, 1, 0]
            return self.move(b[a])
        else:
            b = [3, 0, 1]
            return self.move(b[a])

    def render(self, state = None):
        if state == None:
            state = self.state
        for i in range(self.rows):
            for j in range(self.columns - 1):
                a = int( (i * self.columns) + j)
                if a == state:
                    print( '웃', end=' ' )
                else:
                    print(self.reward_for_certain_state(a), end=' ')
            a = int( (i * self.columns) + j + 1)
            if a == state:
                print( '웃')
            else:
                print( self.reward_for_certain_state( a ))
        print()

    def policy(self, qtable):
        print()
        for i in range( self.rows ):
            for j in range( self.columns - 1 ):
                a = int( (i * self.columns) + j)
                action = np.argmax( qtable[a, :] )
                print( self.action_symbol(action), end=' ' )
            a = int( (i * self.columns) + j + 1)
            action = np.argmax( qtable[a, :] )
            print(self.action_symbol(action))

    def action_symbol(self, action):
        if action == 0:
            return '↑'
        elif action == 1:
            return '↓'
        elif action == 2:
            return '←'
        else:
            return '→'

class frozen_lake_v2:
    def __init__(self):
        self.width = 100
        self.height = 100
        self.rewards = rewards
        self.columns = columns
        self.rows = rows
        self.env = Environment(self.width, self.height, self.rows, self.columns)
        self.fire = []
        self.water = []
        self.brick = []
        self.start = 0
        self.end = 0
        self.possible = []
        for i in range(rows):
            for j in range(columns):
                if self.env.maze[i][j] == 1:
                    self.start = i * columns + j
                elif self.env.maze[i][j] == 2:
                    self.brick.append((i * columns + j))
                elif self.env.maze[i][j] == 3:
                    self.end = i * columns + j
                elif self.env.maze[i][j] == 4:
                    self.fire.append((i * columns + j))
                elif self.env.maze[i][j] == 5:
                    self.water.append((i * columns + j))
                else:
                    self.possible.append((i * columns + j))
        self.slip = 0.33
        self.actions = 4
        self.state = self.start


    def reset(self):
        self.state = self.start
        return self.state

    def get_inputs(self):
        self.rows = int(input())
        self.columns = int(input())
        possible = []
        for i in range(self.rows):
            a = input().split()
            for j in range(self.columns):
                if a[j] == 'f':
                    self.fire.append(i * self.columns + j)
                elif a[j] == 'w':
                    self.water.append(i * self.columns + j)
                elif a[j] == 'b':
                    self.brick.append(i * self.columns + j)
                elif a[j] == 's':
                    self.start = i * self.columns + j
                    possible.append(int( (i * self.columns) + j))
                elif a[j] == 'g':
                    self.end = i * self.columns + j
                else:
                    possible.append( int( (i * self.columns) + j ) )
        self.possible = possible

    def move(self, action):
        s = self.state
        if action == 0:
            if self.state >= self.columns:
                self.state -= self.columns
        elif action == 1:
            if self.state + self.columns <= self.columns * self.rows - 1:
                self.state += self.columns
        elif action == 2:
            if self.state % 4 != 0:
                self.state -= 1
        else:
            if self.state % 4 != 3:
                self.state += 1
        done = False
        if self.state == self.end:
            done = True
        elif self.state in self.fire:
            done = True
        if self.state in self.brick:
            self.state = s
        return self.state, self.reward(), done


    def reward(self):
        for i in range(len(self.fire)):
            if self.state == self.fire[i]:
                return self.rewards['f']
        for i in range(
                len(self.brick)):
            if self.state == self.brick[i]:
                return self.rewards['b']
        for i in range(len(self.water)):
            if self.state == self.water[i]:
                return self.rewards['w']
        if self.state == self.end:
            return self.rewards['g']
        return self.rewards['_']

    def reward_for_certain_state(self, state):
        for i in range(len(self.fire)):
            if state == self.fire[i]:
                return colored('🔥', 'red')
        for i in range(len(self.brick)):
            if state == self.brick[i]:
                return colored('🧇', 'red')
        for i in range(len(self.water)):
            if state == self.water[i]:
                return colored('💧', 'blue')
        if state == self.end:
            return colored('🏁', 'green')
        if state == self.start:
            return colored('⚐', 'white')
        return '_'


    def step(self, action):
        rand = random.random()
        if rand < 1 - (self.slip * 2):
            a = 0
        elif rand < 1 - self.slip:
            a = 1
        else:
            a = 2
        if action == 0:
            b = [0, 2, 3]
            return self.move(b[a])
        elif action == 1:
            b = [1, 3, 2]
            return self.move(b[a])
        elif action == 2:
            b = [2, 1, 0]
            return self.move(b[a])
        else:
            b = [3, 0, 1]
            return self.move(b[a])

    def render(self, state = None):
        if state == None:
            state = self.state
        for i in range(self.rows):
            for j in range(self.columns - 1):
                a = int( (i * self.columns) + j)
                if a == state:
                    print( '웃', end=' ' )
                else:
                    print(self.reward_for_certain_state(a), end=' ')
            a = int( (i * self.columns) + j + 1)
            if a == state:
                print( '웃')
            else:
                print( self.reward_for_certain_state( a ))
        print()

    def policy(self, qtable):
        print()
        for i in range( self.rows ):
            for j in range( self.columns - 1 ):
                a = int( (i * self.columns) + j)
                action = np.argmax( qtable[a, :] )
                print( self.action_symbol(action), end=' ' )
            a = int( (i * self.columns) + j + 1)
            action = np.argmax( qtable[a, :] )
            print(self.action_symbol(action))

    def action_symbol(self, action):
        if action == 0:
            return '↑'
        elif action == 1:
            return '↓'
        elif action == 2:
            return '←'
        else:
            return '→'

    def render_plot(self, states):
        for i in range(len(states)):
            self.env.movePlayer(states[i])
        while True:
            self.env.movePlayer(states[-1])