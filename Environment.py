from SnakeGame import Directions, SnakeGame, LastAction, GameStatus
from enum import Enum
import gymnasium as gym

class Element(Enum):
    EMPTY = 0
    OBSTACLE = 1
    GREEN_APPLE = 2
    RED_APPLE = 3

class Environment(gym.Env):
    game: SnakeGame
    state: tuple
    last_reward: int
    terminated: bool
    interpreter: object  # Référence optionnelle à l'Interpreter

    def __init__(self, game: SnakeGame, interpreter=None):
        if game == None:
            game = SnakeGame()
        self.game = game
        self.interpreter = interpreter
        self.size = game.frame_height
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Tuple((
            gym.spaces.Tuple((gym.spaces.Discrete(4), gym.spaces.Discrete(4), gym.spaces.Discrete(4))), #adjacent elements
            gym.spaces.Tuple((gym.spaces.Discrete(2), gym.spaces.Discrete(2), gym.spaces.Discrete(2))) #green apple presence in the 3 directions
        ))
        self.last_reward = 0
        self.state = self._get_obs()
        self.terminated = False

    def _map_element(self, element):
        if element == 0:
            return Element.EMPTY.value
        elif element == ord('R'):
            return Element.RED_APPLE.value
        elif element == ord('G'):
            return Element.GREEN_APPLE.value
        elif element == ord('W'):
            return Element.OBSTACLE.value
        elif element == ord('S'):
            return Element.OBSTACLE.value
        else:
            return Element.EMPTY.value

    def _get_obs(self):
        """
        Returns the current observation of the snake:
        - a tuple of the elements it can see from its head, clockwise starting from the left, directly adjacent to the head
        - a tuple indicating the presence of a green apple in the 4 cardinal directions, starting from the left and going clockwise
        """
        head_position = self.game.snake[0]
        current_direction = self.game.current_direction
        
        # Map direction to (left_offset, up_offset, right_offset) and (left_row_fn, up_row_fn, right_row_fn)
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
        green_apples = (1 if ord('G') in left_row else 0, 1 if ord('G') in up_row else 0, 1 if ord('G') in right_row else 0)
        return (adjacents, green_apples)

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
        return self._get_obs(), {}

    def step(self, action):
        action_direction = self.map_action_to_direction(action, self.game.current_direction)
        self.game.move_snake(action_direction)
        terminated = self.game.status == GameStatus.GAME_OVER
        state = self._get_obs()
        reward = 0
        if terminated:
            reward = -3
        elif self.game.lastAction == LastAction.GREEN_APPLE:
            reward = 1
        elif self.game.lastAction == LastAction.RED_APPLE:
            reward = -2
        elif self.game.lastAction == LastAction.MOVE:
            reward = 0
        self.last_reward = reward
        self.state = state
        self.terminated = terminated
        if self.interpreter:
            self.interpreter.update(state, reward, terminated, self.game)
        return state, reward, terminated
        