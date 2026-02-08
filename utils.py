import pygame
from SnakeGame import SnakeGame, Directions, GameStatus
from enum import Enum

class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    PURPLE = (128, 0, 128)


def draw_board(surface: pygame.Surface, game: SnakeGame):
    surface.fill(Colors.WHITE.value)
    rect_width = 500 // game.frame_width
    rect_height = 500 // game.frame_height
    for j in range(game.frame_height):
        for i in range(game.frame_width):
            rect = pygame.Rect(25 + i * rect_width, 25 + j * rect_height, rect_width, rect_height)
            if game.board[j * game.frame_width + i] == ord('W'):
                pygame.draw.rect(surface, Colors.PURPLE.value, rect)
            elif game.board[j * game.frame_width + i] == ord('S'):
                pygame.draw.rect(surface, Colors.BLACK.value, rect)
            elif game.board[j * game.frame_width + i] == ord('R'):
                pygame.draw.rect(surface, Colors.RED.value, rect)
            elif game.board[j * game.frame_width + i] == ord('G'):
                pygame.draw.rect(surface, Colors.GREEN.value, rect)
            elif game.board[j * game.frame_width + i] == ord('H'):
                pygame.draw.rect(surface, Colors.BLACK.value, rect, width=10)
            else:
                pygame.draw.rect(surface, Colors.BLACK.value, rect, width=1)