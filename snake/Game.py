import numpy as np
import random
from enum import Enum

class Directions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class GameStatus(Enum):
    RUNNING = 0
    GAME_OVER = 1
    VICTORY = 2

class Game():
    width: int
    height: int
    frame_width: int
    frame_height: int
    board: list[int]
    snake: list[int]
    current_direction: Directions
    status: GameStatus

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
        self.status = GameStatus.RUNNING
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

    def __up(self):
        current_head_position = self.snake[0]
        new_head_position = current_head_position - self.frame_width
        self.print_board()
        # if self.current_direction in [Directions.DOWN, Directions.UP]:
        if self.current_direction in [Directions.DOWN]: #for controls test purposes, to be deleted and replaced with the above line once the snake moves by itself
            print("Cannot move up")
            pass
        elif self.board[new_head_position] == 0:
            self.__update_snake_position(current_head_position, new_head_position)
            self.current_direction = Directions.UP
            print("Moved Up")
        else:
            print("Checking collisions, new head position collides with ", self.board[new_head_position])
            self.__check_collisions(current_head_position, new_head_position, Directions.UP)

    def move_snake(self, direction: Directions):
        if self.status == GameStatus.GAME_OVER:
            print("Game is over. Cannot move the snake.")
            return
        match direction:
            case Directions.UP:
                self.__up()
            case Directions.DOWN:
                self.__down()
            case Directions.LEFT:
                self.__left()
            case Directions.RIGHT:
                self.__right()

    def __down(self):
        current_head_position = self.snake[0]
        new_head_position = current_head_position + self.frame_width
        # if self.current_direction in [Directions.UP, Directions.DOWN]:
        if self.current_direction in [Directions.UP]: #for controls test purposes, to be deleted and replaced with the above line once the snake moves by itself
            print("Cannot move down")
            pass
        elif self.board[new_head_position] == 0:
            self.__update_snake_position(current_head_position, new_head_position)
            self.current_direction = Directions.DOWN
            print("Moved Down")
        else:
            print("Checking collisions, new head position collides with ", self.board[new_head_position])
            self.__check_collisions(current_head_position, new_head_position, Directions.DOWN)
    
    def __left(self):
        current_head_position = self.snake[0]
        new_head_position = current_head_position - 1
        # if self.current_direction in [Directions.RIGHT, Directions.LEFT]:
        if self.current_direction in [Directions.RIGHT]: #for controls test purposes, to be deleted and replaced with the above line once the snake moves by itself
            print("Cannot move left")
            pass
        elif self.board[new_head_position] == 0:
            self.__update_snake_position(current_head_position, new_head_position)
            self.current_direction = Directions.LEFT
            print("Moved Left")
        else:
            print("Checking collisions, new head position collides with ", self.board[new_head_position])
            self.__check_collisions(current_head_position, new_head_position, Directions.LEFT)
    
    def __right(self):
        current_head_position = self.snake[0]
        new_head_position = current_head_position + 1
        # if self.current_direction in [Directions.LEFT, Directions.RIGHT]:
        if self.current_direction in [Directions.LEFT]: #for controls test purposes, to be deleted and replaced with the above line once the snake moves by itself
            print("Cannot move right")
            pass
        elif self.board[new_head_position] == 0:
            self.__update_snake_position(current_head_position, new_head_position)
            self.current_direction = Directions.RIGHT
            print("Moved Right")
        else:
            print("Checking collisions, new head position collides with ", self.board[new_head_position])
            self.__check_collisions(current_head_position, new_head_position, Directions.RIGHT)

    def __update_snake_position(self, current_head_position: int, new_head_position: int):
        self.snake.insert(0, new_head_position)
        self.board[new_head_position] = ord('H')
        self.board[current_head_position] = ord('S')
        tail_position = self.snake[-1]
        self.board[tail_position] = 0
        self.snake.pop()
    
    def __grow_snake(self):
        current_tail_position = self.snake[-1]
        second_last_tail_position = self.snake[-2]
        direction_vector = current_tail_position - second_last_tail_position
        match direction_vector:
            case self.frame_width:
                # going up
                new_tail_position = current_tail_position + self.frame_width
                if self.board[new_tail_position] != 0:
                    if self.board[current_tail_position + 1] == 0:
                        new_tail_position = current_tail_position + 1
                    else:
                        new_tail_position = current_tail_position - 1
            case x if x == -(self.frame_width):
                # going down
                new_tail_position = current_tail_position - self.frame_width
                if self.board[new_tail_position] != 0:
                    if self.board[current_tail_position + 1] == 0:
                        new_tail_position = current_tail_position + 1
                    else:
                        new_tail_position = current_tail_position - 1
            case 1:
                # going left
                new_tail_position = current_tail_position + 1
                if self.board[new_tail_position] != 0:
                    if self.board[current_tail_position + self.frame_width] == 0:
                        new_tail_position = current_tail_position + self.frame_width
                    else:
                        new_tail_position = current_tail_position - self.frame_width
            case -1:
                # going right
                new_tail_position = current_tail_position - 1
                if self.board[new_tail_position] != 0:
                    if self.board[current_tail_position + self.frame_width] == 0:
                        new_tail_position = current_tail_position + self.frame_width
                    else:
                        new_tail_position = current_tail_position - self.frame_width
        self.snake.append(new_tail_position)
        self.board[new_tail_position] = ord('S')
    
    def __reduce_snake(self):
        tail_position = self.snake[-1]
        self.board[tail_position] = 0
        self.snake.pop()

    def __check_collisions(self, current_head_position: int, new_head_position: int, direction: Directions):
        if self.board[new_head_position] == ord('W') or self.board[new_head_position] == ord('S'):
            self.status = GameStatus.GAME_OVER
            print("Game Over!")
        elif self.board[new_head_position] == ord('G'):
            self.__grow_snake()
            self.__update_snake_position(current_head_position, new_head_position)
            self.current_direction = direction
            self.__spawn_new_apple('G')
        elif self.board[new_head_position] == ord('R'):
            if (len(self.snake) == 1):
                self.status = GameStatus.GAME_OVER
                print("Game Over!")
            else:
                self.__reduce_snake()
                self.__update_snake_position(current_head_position, new_head_position)
                self.current_direction = direction
                self.__spawn_new_apple('R')
    
    def __spawn_new_apple(self, apple_type: str):
        if apple_type not in ['R', 'G']:
            raise ValueError("Invalid apple type")
        # current_pos = self.board.index(ord(apple_type))
        current_pos = np.where(self.board == ord(apple_type))
        print("Current apple position(s): ", current_pos)
        new_apple_position: int = random.randint(0, self.width * self.height - 1)
        while self.board[new_apple_position] != 0:
            new_apple_position = random.randint(0, self.width * self.height - 1)
        self.board[new_apple_position] = ord(apple_type)
        self.board[current_pos] = 0
    