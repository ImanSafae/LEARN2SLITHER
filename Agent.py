import time
import numpy as np
from SnakeGame import SnakeGame, GameStatus
from Environment import Environment
from Interpreter import Interpreter

class Agent():

    q_table: np.ndarray
    environment: Environment
    interpreter: Interpreter
    epsilon: int
    learning_rate: int
    discount: int

    def __init__(self, environment: Environment, interpreter: Interpreter, learning_rate=0.01, epsilon=0.2, discount=0.99):
        self.environment = environment
        self.interpreter = interpreter
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount = discount
        self.q_table = {}  # Dictionnaire vide : {state: [q_values pour chaque action]}


    def q(self, state, action, reward):
        # Initialiser l'état s'il n'existe pas
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.environment.action_space.n)
        
        current_q_value = self.q_table[state][action]
        max_future_q = np.max(self.q_table[state])
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount * max_future_q)
        return new_q_value
        

    def choose_action(self, state):
        # Initialiser l'état s'il n'existe pas
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.environment.action_space.n)
        
        random_number = np.random.rand()
        if random_number < self.epsilon:
            # exploration
            print("Exploration: choosing random action")
            action = np.random.choice(self.environment.action_space.n)
        else:
            # exploitation
            action = np.argmax(self.q_table[state])
        return action
    
    def learn(self):
        if self.environment.game.status == GameStatus.GAME_OVER:
            self.environment.reset()
        episode_over = False
        state = self.environment._get_obs()
        while not episode_over:
            action = self.choose_action(state)
            self.environment.step(action)
            state, reward, terminated = self.interpreter.get_step_result()
            q_value = self.q(state, action, reward)
            self.q_table[state][action] = q_value
            episode_over = terminated
            time.sleep(0.25)
        
    def train(self, episodes):
        for episode in range(episodes):
            self.learn()
        

    
        
