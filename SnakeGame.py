import numpy as np
import random
from enum import Enum


class Directions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class GameStatus(Enum):
    WAITING = 0
    RUNNING = 1
    GAME_OVER = 2
    VICTORY = 3


class LastAction(Enum):
    MOVE = 0
    GREEN_APPLE = 1
    RED_APPLE = 2
    LOST = 3
    NONE = 4


class SnakeGame():
    width: int
    height: int
    frame_width: int
    frame_height: int
    board: list[int]
    snake: list[int]
    current_direction: Directions
    status: GameStatus
    lastAction: LastAction

    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.frame_width = self.width + 2
        self.frame_height = self.height + 2
        self.board = np.zeros(
            self.frame_width * self.frame_height, dtype=int)
        self.__init_walls()
        self.__init_snake()
        self.__init_apples()
        self.current_direction = Directions.UP
        self.status = GameStatus.WAITING
        self.lastAction = LastAction.NONE

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
        head_position: int = random.randint(
            0, self.width * self.height - 1)
        while self.board[head_position] != 0:
            head_position = random.randint(
                0, self.width * self.height - 1)
        self.snake = [
            head_position,
            head_position + self.width + 2,
            head_position + 2 * (self.width + 2)]
        self.board[head_position] = ord('H')
        self.board[head_position + self.width + 2] = ord('S')
        self.board[head_position + 2 * (self.width + 2)] = ord('S')

    def __init_apples(self):
        max_pos = self.width * self.height - 1
        red_pos: int = random.randint(0, max_pos)
        while (red_pos in self.snake
               or self.board[red_pos] != 0):
            red_pos = random.randint(0, max_pos)
        self.board[red_pos] = ord('R')
        green_pos: int = random.randint(0, max_pos)
        while self.board[green_pos] != 0:
            green_pos = random.randint(0, max_pos)
        self.board[green_pos] = ord('G')
        green_pos: int = random.randint(0, max_pos)
        while self.board[green_pos] != 0:
            green_pos = random.randint(0, max_pos)
        self.board[green_pos] = ord('G')

    def print_board(self):
        fw: int = self.width + 2
        fh: int = self.height + 2
        for i in range(fh):
            row = self.board[i * fw:(i + 1) * fw]
            print(" ".join(
                str(c) if c == 0 else chr(c)
                for c in row
            ))

    def __up(self):
        if self.status == GameStatus.GAME_OVER:
            print("Game is over. Cannot move the snake.")
            return
        cur = self.snake[0]
        new = cur - self.frame_width
        # if self.current_direction in
        # [Directions.DOWN, Directions.UP]:
        if (self.current_direction == Directions.DOWN
                and len(self.snake) > 1):  # tmp
            print("Cannot move up")
        elif self.board[new] == 0:
            self.__update_snake_position(cur, new)
            self.current_direction = Directions.UP
            self.lastAction = LastAction.MOVE
        else:
            self.__check_collisions(
                cur, new, Directions.UP
            )

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
        if self.status == GameStatus.GAME_OVER:
            print("Game is over. Cannot move the snake.")
            return
        cur = self.snake[0]
        new = cur + self.frame_width
        # if self.current_direction in
        # [Directions.UP, Directions.DOWN]:
        if (self.current_direction == Directions.UP
                and len(self.snake) > 1):  # tmp
            print("Cannot move down")
            pass
        elif self.board[new] == 0:
            self.__update_snake_position(cur, new)
            self.current_direction = Directions.DOWN
            self.lastAction = LastAction.MOVE
        else:
            self.__check_collisions(
                cur, new, Directions.DOWN
            )

    def __left(self):
        if self.status == GameStatus.GAME_OVER:
            print("Game is over. Cannot move the snake.")
            return
        cur = self.snake[0]
        new = cur - 1
        # if self.current_direction in
        # [Directions.RIGHT, Directions.LEFT]:
        if (self.current_direction == Directions.RIGHT
                and len(self.snake) > 1):  # tmp
            print("Cannot move left")
            pass
        elif self.board[new] == 0:
            self.__update_snake_position(cur, new)
            self.current_direction = Directions.LEFT
            self.lastAction = LastAction.MOVE
        else:
            self.__check_collisions(
                cur, new, Directions.LEFT
            )

    def __right(self):
        if self.status == GameStatus.GAME_OVER:
            print("Game is over. Cannot move the snake.")
            return
        cur = self.snake[0]
        new = cur + 1
        # if self.current_direction in
        # [Directions.LEFT, Directions.RIGHT]:
        if (self.current_direction == Directions.LEFT
                and len(self.snake) > 1):  # tmp
            print("Cannot move right")
            pass
        elif self.board[new] == 0:
            self.__update_snake_position(cur, new)
            self.current_direction = Directions.RIGHT
            self.lastAction = LastAction.MOVE
        else:
            self.__check_collisions(
                cur, new, Directions.RIGHT
            )

    def __update_snake_position(
        self, current_head_position: int,
        new_head_position: int
    ):
        if self.status == GameStatus.GAME_OVER:
            print("Game is over. Cannot move the snake.")
            return
        self.snake.insert(0, new_head_position)
        self.board[new_head_position] = ord('H')
        self.board[current_head_position] = ord('S')
        tail_position = self.snake[-1]
        self.board[tail_position] = 0
        self.snake.pop()

    def __grow_snake(self):
        if self.status == GameStatus.GAME_OVER:
            print("Game is over. Cannot grow the snake.")
            return
        empty_cells = np.where(self.board == 0)[0]
        if len(empty_cells) == 1:
            print("No empty cell available to grow the snake!")
            self.status = GameStatus.VICTORY
            return
        if len(self.snake) == 1:
            current_head_position = self.snake[0]
            match self.current_direction:
                case Directions.UP:
                    new_tail_position = (
                        current_head_position
                        + self.frame_width)
                case Directions.DOWN:
                    new_tail_position = (
                        current_head_position
                        - self.frame_width)
                case Directions.LEFT:
                    new_tail_position = current_head_position + 1
                case Directions.RIGHT:
                    new_tail_position = current_head_position - 1
            self.snake.append(new_tail_position)
            self.board[new_tail_position] = ord('S')
            return
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
                new_tail_position = (
                    current_tail_position + 1)
                if self.board[new_tail_position] != 0:
                    fw = self.frame_width
                    if self.board[
                        current_tail_position + fw
                    ] == 0:
                        new_tail_position = (
                            current_tail_position + fw)
                    else:
                        new_tail_position = (
                            current_tail_position - fw)
            case -1:
                # going right
                new_tail_position = (
                    current_tail_position - 1)
                if self.board[new_tail_position] != 0:
                    fw = self.frame_width
                    if self.board[
                        current_tail_position + fw
                    ] == 0:
                        new_tail_position = (
                            current_tail_position + fw)
                    else:
                        new_tail_position = (
                            current_tail_position - fw)
        self.snake.append(new_tail_position)
        self.board[new_tail_position] = ord('S')

    def __reduce_snake(self):
        if self.status == GameStatus.GAME_OVER:
            print("Game is over. Cannot reduce the snake.")
            return
        tail_position = self.snake[-1]
        self.board[tail_position] = 0
        self.snake.pop()

    def __check_collisions(
        self, current_head_position: int,
        new_head_position: int,
        direction: Directions
    ):
        cell = self.board[new_head_position]
        if cell == ord('W') or cell == ord('S'):
            self.status = GameStatus.GAME_OVER
            self.lastAction = LastAction.LOST
        elif cell == ord('G'):
            self.lastAction = LastAction.GREEN_APPLE
            self.current_direction = direction
            self.__grow_snake()
            if self.status == GameStatus.VICTORY:
                return
            self.__spawn_new_apple(
                new_head_position, 'G')
            self.__update_snake_position(
                current_head_position,
                new_head_position)
        elif cell == ord('R'):
            if len(self.snake) == 1:
                self.status = GameStatus.GAME_OVER
                self.lastAction = LastAction.LOST
            else:
                self.__reduce_snake()
                self.current_direction = direction
                self.__spawn_new_apple(
                    new_head_position, 'R')
                self.__update_snake_position(
                    current_head_position,
                    new_head_position)
                self.lastAction = LastAction.RED_APPLE

    def __spawn_new_apple(self, current_pos, apple_type: str):
        if self.status == GameStatus.GAME_OVER:
            print("Game is over. Cannot spawn any apple.")
            return
        if apple_type not in ['R', 'G']:
            raise ValueError("Invalid apple type")
        # current_pos = np.where(self.board == ord(apple_type))
        # print("Current apple position(s): ", current_pos)
        empty_cells = np.where(self.board == 0)[0]
        new_apple_position: int = np.random.choice(empty_cells)
        while self.board[new_apple_position] != 0:
            new_apple_position: int = np.random.choice(empty_cells)
        self.board[new_apple_position] = ord(apple_type)
        self.board[current_pos] = 0

    def get_left_row(self):
        row = []
        head_pos = self.snake[0]
        i = head_pos - 1
        closest_left_wall = head_pos - (head_pos % self.frame_width)
        while i >= closest_left_wall:
            row.append(self.board[i])
            i -= 1
        return row

    def get_right_row(self):
        row = []
        head_pos = self.snake[0]
        i = head_pos + 1
        mod = head_pos % self.frame_width
        closest_right_wall = (
            head_pos + (self.frame_width - mod) - 1)
        while i <= closest_right_wall:
            row.append(self.board[i])
            i += 1
        return row

    def get_up_row(self):
        row = []
        head_pos = self.snake[0]
        i = head_pos - self.frame_width
        while i >= 0:
            row.append(self.board[i])
            i -= self.frame_width
        return row

    def get_down_row(self):
        row = []
        head_pos = self.snake[0]
        i = head_pos + self.frame_width
        while i < len(self.board):
            row.append(self.board[i])
            i += self.frame_width
        return row
