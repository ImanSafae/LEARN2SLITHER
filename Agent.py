import time
import numpy as np
from SnakeGame import SnakeGame, GameStatus
from Environment import Element, Environment
from Interpreter import Interpreter

class Agent():

    q_table: dict
    environment: Environment
    interpreter: Interpreter
    epsilon: float
    learning_rate: float
    discount: float
    last_snake_length: int
    lengths_history: list
    sleep_time: float

    def __init__(self, environment: Environment, interpreter: Interpreter, learning_rate=0.15, epsilon=1.0, discount=0.95, decay_rate=0.9998, q_table=None, sleep_time=None):
        self.environment = environment
        self.interpreter = interpreter
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.decay_rate = decay_rate
        self.discount = discount
        self.q_table = q_table if q_table is not None else {}
        self.last_snake_length = 0
        self.lengths_history = []
        self.sleep_time = sleep_time

    def q(self, state, action, reward, next_state):
        if state not in self.q_table:
            if state == ((Element.DEATH.value, Element.DEATH.value, Element.DEATH.value), (0, 0, 0)):
                self.q_table[state] = np.zeros(self.environment.action_space.n) - 1000
            else:
                self.q_table[state] = np.zeros(self.environment.action_space.n)
        if next_state not in self.q_table:
            if next_state == ((Element.DEATH.value, Element.DEATH.value, Element.DEATH.value), (0, 0, 0)):
                print("State of death encountered")
                self.q_table[next_state] = np.zeros(self.environment.action_space.n) - 1000
            else:
                self.q_table[next_state] = np.zeros(self.environment.action_space.n)
        
        current_q_value = self.q_table[state][action]
        max_future_q = np.max(self.q_table[next_state])
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount * max_future_q)
        return new_q_value
    
    def decay_epsilon(self):
        self.epsilon *= self.decay_rate
        if self.epsilon < 0.1:
            self.epsilon = 0.1

    def choose_action(self, state):
        if state not in self.q_table:
            # print("New state encountered! :", state)
            self.q_table[state] = np.zeros(self.environment.action_space.n)
        
        random_number = np.random.rand()
        if random_number < self.epsilon:
            # exploration
            # print("Exploration: choosing random action")
            action = np.random.choice(self.environment.action_space.n)
        else:
            # exploitation
            action = np.argmax(self.q_table[state])
        return action
    
    def learn(self):
        # if self.environment.game.status == GameStatus.GAME_OVER:
        episode_over = False
        state = self.environment.state
        while not episode_over:
            action = self.choose_action(state)
            self.environment.step(action)
            next_state, reward, terminated = self.interpreter.get_step_result()
            q_value = self.q(state, action, reward, next_state)
            self.q_table[state][action] = q_value
            episode_over = terminated
            state = next_state
            if self.sleep_time:
                time.sleep(self.sleep_time)
            # time.sleep(0.25)
        self.lengths_history.append(len(self.environment.game.snake))
        self.last_snake_length = len(self.environment.game.snake)
        self.environment.reset()
        
    def train(self, episodes):
        for episode in range(episodes):
            self.learn()
            self.decay_epsilon()
            if episode % 1000 == 0:
                recent_lengths = self.lengths_history[-100:] if len(self.lengths_history) >= 100 else self.lengths_history
                avg_length = sum(recent_lengths) / len(recent_lengths) if recent_lengths else 0
                print(f"Episode {episode}: avg_length={avg_length:.2f}, epsilon={self.epsilon:.3f}, q_table_size={len(self.q_table)}")

    def exploit(self, q_table: np.ndarray, display_mode=True, sleep_time=0.75, nb_of_rounds=10):
        self.q_table = q_table
        self.epsilon = 0.0
        self.sleep_time = sleep_time
        self.interpreter.display_mode = display_mode
        if display_mode:
            self.interpreter.init_pygame()
        for _ in range(nb_of_rounds):
            self.environment.reset()
            episode_over = False
            state = self.environment.state
            while not episode_over:
                action = self.choose_action(state)
                self.environment.step(action)
                next_state, reward, terminated = self.interpreter.get_step_result()
                state = next_state
                episode_over = terminated
                if self.sleep_time:
                    print(f"Sleeping for {self.sleep_time} seconds...")
                    time.sleep(self.sleep_time)

    
        
