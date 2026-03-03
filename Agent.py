import time
import numpy as np
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
    step_by_step: bool
    print_actions_mode: bool

    def __init__(self, environment: Environment,
                 interpreter: Interpreter, learning_rate=0.15,
                 epsilon=1.0, discount=0.95, decay_rate=0.9998,
                 q_table=None, sleep_time=None, step_by_step=False,
                 print_actions_mode=False):
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
        self.step_by_step = step_by_step
        self.print_actions_mode = print_actions_mode
        self.action_history = []

    def q(self, state, action, reward, next_state):
        death_state = ((Element.DEATH.value, Element.DEATH.value,
                        Element.DEATH.value), (0, 0, 0))
        if state not in self.q_table:
            if state == death_state:
                n = self.environment.action_space.n
                self.q_table[state] = np.zeros(n) - 1000
            else:
                self.q_table[state] = (
                    np.zeros(self.environment.action_space.n))
        if next_state not in self.q_table:
            if next_state == death_state:
                print("State of death encountered")
                n = self.environment.action_space.n
                self.q_table[next_state] = np.zeros(n) - 1000
            else:
                self.q_table[next_state] = (
                    np.zeros(self.environment.action_space.n))
        current_q_value = self.q_table[state][action]
        max_future_q = np.max(self.q_table[next_state])
        new_q_value = ((1 - self.learning_rate) * current_q_value +
                       self.learning_rate *
                       (reward + self.discount * max_future_q))
        return new_q_value

    def decay_epsilon(self):
        self.epsilon *= self.decay_rate
        if self.epsilon < 0.1:
            self.epsilon = 0.1

    def _is_looping(self):
        head = self.environment.game.snake[0]
        self.position_history.append(head)
        if len(self.position_history) > 20:
            self.position_history = self.position_history[-20:]
        if len(self.position_history) < 8:
            return False
        recent = self.position_history[-8:]
        unique = len(set(recent))
        return unique <= 4

    def choose_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(
                self.environment.action_space.n)
        random_number = np.random.rand()
        is_looping = (self.epsilon == 0
                      and self._is_looping())
        if random_number < self.epsilon:
            action = np.random.choice(
                self.environment.action_space.n)
        elif is_looping:
            # Force a different action than last one
            last = (self.action_history[-1]
                    if self.action_history else -1)
            choices = [a for a in range(
                self.environment.action_space.n)
                if a != last]
            action = np.random.choice(choices)
        else:
            best_values = np.max(self.q_table[state])
            best_actions = np.where(
                self.q_table[state] == best_values)[0]
            action = np.random.choice(best_actions)
        self.action_history.append(action)
        if len(self.action_history) > 20:
            self.action_history = self.action_history[-20:]
        return action

    def print_action(self, action):
        direction_txt = ""
        if action == 0:
            direction_txt = "LEFT"
        elif action == 1:
            direction_txt = "STRAIGHT"
        elif action == 2:
            direction_txt = "RIGHT"
        print(f"Action taken: {direction_txt}")

    def _reverse_map_element(self, element: Element):
        if element == Element.EMPTY.value:
            return "0"
        elif element == Element.GREEN_APPLE.value:
            return "G"
        elif element == Element.RED_APPLE.value:
            return "R"
        elif element == Element.DANGER.value:
            return "D"
        elif element == Element.DEATH.value:
            return "X"
        return "0"

    def print_view(self, state):
        # print("State:", state)
        # first tuple = adjacents
        # second tuple = distance to closest apple in every direction
        adjacents = state[0]
        dist_to_apples = state[1]
        dist_to_apple_forward = dist_to_apples[1]
        dist_to_apple_left = dist_to_apples[0]
        dist_to_apple_right = dist_to_apples[2]

        fwd_info = ""
        if dist_to_apple_forward == 1:
            fwd_info = "Apple close ahead!"
        elif dist_to_apple_forward == 2:
            fwd_info = "Apple far ahead!"
        fwd_elem = self._reverse_map_element(adjacents[1])
        print(f"{'':<24}{fwd_info}")
        print(f"{'':<31}{fwd_elem}")

        left_info = ""
        if dist_to_apple_left == 1:
            left_info = "Apple close on the left!"
        elif dist_to_apple_left == 2:
            left_info = "Apple far on the left!"
        right_info = ""
        if dist_to_apple_right == 1:
            right_info = "Apple close on the right!"
        elif dist_to_apple_right == 2:
            right_info = "Apple far on the right!"
        row = (f"{self._reverse_map_element(adjacents[0])}"
               + "H" + f"{self._reverse_map_element(adjacents[2])}")
        print(f"{left_info:<30}{row:<10}{right_info}")
        print("-------------------------------------")

    def learn(self):
        episode_over = False
        state = self.environment.state
        self.action_history = []
        self.position_history = []
        while not episode_over:
            action = self.choose_action(state)
            self.environment.step(action)
            next_state, reward, terminated = self.interpreter.get_step_result()
            q_value = self.q(state, action, reward, next_state)
            self.q_table[state][action] = q_value
            episode_over = terminated
            state = next_state
            if self.print_actions_mode:
                self.print_action(action)
                self.print_view(state)
            if self.sleep_time:
                time.sleep(self.sleep_time)
        self.lengths_history.append(len(self.environment.game.snake))
        self.last_snake_length = len(self.environment.game.snake)
        self.environment.reset()

    def train(self, episodes):
        for episode in range(episodes):
            self.learn()
            self.decay_epsilon()
            if episode % 1000 == 0:
                if len(self.lengths_history) >= 100:
                    recent_lengths = self.lengths_history[-100:]
                else:
                    recent_lengths = self.lengths_history
                avg_length = (sum(recent_lengths) / len(recent_lengths)
                              if recent_lengths else 0)
                print(f"Episode {episode}: avg_length={avg_length:.2f}, "
                      f"epsilon={self.epsilon:.3f}, "
                      f"q_table_size={len(self.q_table)}")

    def exploit(self, q_table: np.ndarray, display_mode=True,
                sleep_time=0.75, nb_of_rounds=10):
        if q_table is not None:
            self.q_table = q_table
        self.epsilon = 0.0
        self.sleep_time = sleep_time
        self.interpreter.display_mode = display_mode
        if display_mode:
            self.interpreter.init_pygame()
        for _ in range(nb_of_rounds):
            self.environment.reset()
            self.action_history = []
            self.position_history = []
            episode_over = False
            state = self.environment.state
            while not episode_over:
                action = self.choose_action(state)
                self.environment.step(action)
                next_state, reward, terminated = (
                    self.interpreter.get_step_result())
                state = next_state
                if self.print_actions_mode:
                    self.print_action(action)
                    self.print_view(state)
                episode_over = terminated
                if terminated:
                    score = len(self.environment.game.snake)
                    self.lengths_history.append(score)
                    self.last_snake_length = score
                    if not self.step_by_step:
                        time.sleep(0.5)
                elif self.sleep_time and not self.step_by_step:
                    # print(f"Sleeping for {self.sleep_time} seconds...")
                    time.sleep(self.sleep_time)
        if display_mode:
            self.interpreter.show_exploit_summary(self.lengths_history)
