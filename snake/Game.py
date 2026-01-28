import numpy as np
import random
from enum import Enum

class Directions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Statuses(Enum):
    RUNNING = 0
    GAME_OVER = 1

class Game():
    width: int
    height: int
    frame_width: int
    frame_height: int
    board: list[int]
    snake: list[int]
    current_direction: Directions
    status: Statuses

    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.frame_width = self.width + 2
        self.frame_height = self.height + 2
        self.board = np.zeros(self.frame_width * self.frame_height, dtype=int)
        print(f"Initialized board of size {self.width}x{self.height}: {len(self.board)}")
        self.__init_walls()
        self.__init_snake()
        self.__init_apples()
        self.current_direction = Directions.UP
        self.status = Statuses.RUNNING
    def __init_walls(self):
        frame_width: int = self.width + 2
        frame_height: int = self.height + 2
        i: int = 0
        while i < frame_width:
            self.board[i] = ord('W')
            i += 1
        i = (frame_height * frame_width) - 1
        j = frame_width
        while j > 0:
            self.board[i] = ord('W')
            i -= 1
            j -= 1
        i = 0
        while i < frame_height:
            self.board[i * frame_width] = ord('W')
            i += 1
        i = frame_height
        while i > 0:
            self.board[(i * frame_width) - 1] = ord('W')
            i -= 1
    
    def __init_snake(self):
        head_position: int = random.randint(0, self.width * self.height - 1)
        while self.board[head_position] != 0:
            head_position = random.randint(0, self.width * self.height - 1)
        self.snake = [head_position, head_position + self.width + 2, head_position + 2 * (self.width + 2)]
        self.board[head_position] = ord('H')
        self.board[head_position + self.width + 2] = ord('S')
        self.board[head_position + 2 * (self.width + 2)] = ord('S')

    def __init_apples(self):
        red_apple_position: int = random.randint(0, self.width * self.height - 1)
        while red_apple_position in self.snake or self.board[red_apple_position] != 0:
            red_apple_position = random.randint(0, self.width * self.height - 1)
        self.board[red_apple_position] = ord('R')
        green_apple_position: int = random.randint(0, self.width * self.height - 1)
        while green_apple_position in self.snake or green_apple_position == red_apple_position or self.board[green_apple_position] != 0:
            green_apple_position = random.randint(0, self.width * self.height - 1)
        self.board[green_apple_position] = ord('G')

    def print_board(self):
        frame_width: int = self.width + 2
        frame_height: int = self.height + 2
        for i in range(frame_height):
            row = self.board[i * frame_width:(i + 1) * frame_width]
            print(" ".join(str(cell) if cell == 0 else chr(cell) for cell in row))

    def up(self):
        current_head_position = self.snake[0]
        new_head_position = current_head_position - self.frame_width
        if self.current_direction in [Directions.DOWN, Directions.UP]:
            pass
        elif self.board[new_head_position] is 0:
            self.update_snake_position(current_head_position, new_head_position)
        else:
            self.check_collisions(current_head_position, new_head_position)

    def update_snake_position(self, current_head_position: int, new_head_position: int):
        pass

    def check_collisions(self, current_head_position: int, new_head_position: int):
        if self.board[new_head_position] == ord('W'):
            self.status = Statuses.GAME_OVER 
    