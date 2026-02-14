from SnakeGame import Directions, SnakeGame, LastAction, GameStatus
from enum import Enum
import gymnasium as gym

class Element(Enum):
    EMPTY = 0
    DANGER = 1
    GREEN_APPLE = 2
    RED_APPLE = 3
    DEATH = 4

class Environment(gym.Env):
    game: SnakeGame
    state: tuple
    last_reward: int
    terminated: bool
    interpreter: object
    steps: int
    max_steps: int
    death_reason: str

    def __init__(self, game: SnakeGame, interpreter=None, max_steps=200):
        if game == None:
            game = SnakeGame()
        self.game = game
        self.interpreter = interpreter
        self.size = game.frame_width
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Tuple((
            gym.spaces.Tuple((gym.spaces.Discrete(3), gym.spaces.Discrete(3), gym.spaces.Discrete(4))), #adjacent elements: EMPTY/DANGER/GREEN_APPLE/RED_APPLE
            gym.spaces.Tuple((gym.spaces.Discrete(3), gym.spaces.Discrete(3), gym.spaces.Discrete(3))) #distance bins to green apple: 0/1/2
        ))
        self.last_reward = 0
        self.state = self._get_obs()
        self.terminated = False
        self.steps = 0
        self.max_steps = max_steps
        self.death_reason = ""

    def _map_element(self, element):
        if element == 0:
            return Element.EMPTY.value
        elif element == ord('R'):
            return Element.DANGER.value
        elif element == ord('G'):
            return Element.GREEN_APPLE.value
        elif element == ord('W'):
            return Element.DANGER.value
        elif element == ord('S'):
            return Element.DANGER.value
        else:
            return Element.EMPTY.value
        
    def _distance_to_green_apple(self, row):
        if not ord('G') in row:
            return 0
        distance = row.index(ord('G')) + 1
        if distance <= 3:
            return 1
        # elif distance <= 5:
        #     return 2
        else:
            return 2

    def _get_obs(self):
        """
        Returns the current observation of the snake:
        - a tuple of the elements it can see from its head, clockwise starting from the left, directly adjacent to the head
        - a tuple indicating the presence of a green apple in the 4 cardinal directions, starting from the left and going clockwise
        - a tuple indicating the distance to a green apple in the 4 cardinal directions, starting from the left and going clockwise
        """
        if self.game.status == GameStatus.GAME_OVER:
            return ((Element.DEATH.value, Element.DEATH.value, Element.DEATH.value), (0, 0, 0))
        head_position = self.game.snake[0]
        current_direction = self.game.current_direction
        direction_map = {
            Directions.UP: ((-1, -self.size, +1), (self.game.get_left_row, self.game.get_up_row, self.game.get_right_row)),
            Directions.DOWN: ((+1, +self.size, -1), (self.game.get_right_row, self.game.get_down_row, self.game.get_left_row)),
            Directions.LEFT: ((+self.size, -1, -self.size), (self.game.get_down_row, self.game.get_left_row, self.game.get_up_row)),
            Directions.RIGHT: ((-self.size, +1, +self.size), (self.game.get_up_row, self.game.get_right_row, self.game.get_down_row))
        }
        
        offsets, row_functions = direction_map[current_direction]
        left_pos, up_pos, right_pos = [head_position + offset for offset in offsets]
        left_row, up_row, right_row = [fn() for fn in row_functions]
        
        left_element = self._map_element(self.game.board[left_pos])
        up_element = self._map_element(self.game.board[up_pos])
        right_element = self._map_element(self.game.board[right_pos])
        
        
        adjacents = (left_element, up_element, right_element)
        # green_apples = (1 if ord('G') in left_row else 0, 1 if ord('G') in up_row else 0, 1 if ord('G') in right_row else 0)
        distance_to_apples = (self._distance_to_green_apple(left_row), self._distance_to_green_apple(up_row), self._distance_to_green_apple(right_row))
        # print("distance to green apple in the 3 directions (left, up, right):", distance_to_apples)
        return (adjacents, distance_to_apples)

    def map_action_to_direction(self, action, current_direction):
        directions = [Directions.LEFT, Directions.UP, Directions.RIGHT, Directions.DOWN]
        current_index = directions.index(current_direction)
        # action 0 = gauche (-1), action 1 = tout droit (0), action 2 = droite (+1)
        offset = action - 1
        new_index = (current_index + offset) % 4
        return directions[new_index]
        
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        del self.game
        self.game = SnakeGame()
        self._agent_location = self.game.snake[0]
        self.steps = 0
        self.terminated = False
        self.state = self._get_obs()
        self.last_reward = 0
        return self._get_obs(), {}

    def step(self, action):
        self.steps += 1
        old_min_dist = min([d for d in self.state[1] if d > 0], default=0)
        action_direction = self.map_action_to_direction(action, self.game.current_direction)
        self.game.move_snake(action_direction)
        if self.steps >= self.max_steps:
            self.game.status = GameStatus.GAME_OVER
            self.death_reason = "max steps exceeded"
        elif self.game.status == GameStatus.GAME_OVER and self.steps < self.max_steps:
            self.death_reason = "collision"
        terminated = self.game.status == GameStatus.GAME_OVER
        state = self._get_obs()
        new_min_dist = min([d for d in state[1] if d > 0], default=0)
        reward = 0
        if terminated:
            reward = -100
        elif self.game.lastAction == LastAction.GREEN_APPLE:
            reward = 100
        elif self.game.lastAction == LastAction.RED_APPLE:
            reward = -30
        elif self.game.lastAction == LastAction.MOVE:
            # reward = -1
            if old_min_dist > 0 and new_min_dist > 0:
                if new_min_dist < old_min_dist:
                    reward = 5
                elif new_min_dist > old_min_dist:
                    reward = -10
                else:
                    reward = -5
            else:
                reward = -5
        current_length = len(self.game.snake)
        if current_length >= 10:
            reward += (current_length - 9) * 3
        self.last_reward = reward
        self.state = state
        self.terminated = terminated
        if self.interpreter:
            self.interpreter.update(state, reward, terminated, self.game)
        return state, reward, terminated
        