import pygame
from enum import Enum
from SnakeGame import SnakeGame


class Colors(Enum):
    BACKGROUND = (240, 248, 255)
    GRID_LIGHT = (200, 220, 240)
    GRID_DARK = (180, 200, 220)

    WALL_MAIN = (60, 60, 90)
    WALL_BORDER = (40, 40, 70)
    WALL_HIGHLIGHT = (80, 80, 120)

    SNAKE_HEAD = (40, 180, 99)
    SNAKE_HEAD_DARK = (30, 140, 80)
    SNAKE_BODY = (52, 211, 153)
    SNAKE_BODY_LIGHT = (110, 231, 183)
    SNAKE_OUTLINE = (16, 120, 70)

    RED_APPLE = (239, 68, 68)
    RED_APPLE_DARK = (185, 28, 28)
    RED_APPLE_SHINE = (248, 113, 113)
    GREEN_APPLE = (34, 197, 94)
    GREEN_APPLE_DARK = (21, 128, 61)
    GREEN_APPLE_SHINE = (134, 239, 172)

    TEXT_VICTORY = (34, 197, 94)
    TEXT_GAME_OVER = (239, 68, 68)
    TEXT_SHADOW = (100, 100, 100)


def draw_board(surface: pygame.Surface, game: SnakeGame):
    surface.fill(Colors.BACKGROUND.value)

    rect_width = 500 // game.frame_width
    rect_height = 500 // game.frame_height

    for j in range(game.frame_height):
        for i in range(game.frame_width):
            x = 25 + i * rect_width
            y = 25 + j * rect_height
            rect = pygame.Rect(x, y, rect_width, rect_height)
            if game.board[j * game.frame_width + i] != ord('W'):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(surface, Colors.GRID_LIGHT.value, rect)
                else:
                    pygame.draw.rect(surface, Colors.GRID_DARK.value, rect)
    for j in range(game.frame_height):
        for i in range(game.frame_width):
            x = 25 + i * rect_width
            y = 25 + j * rect_height
            rect = pygame.Rect(x, y, rect_width, rect_height)
            inner_rect = pygame.Rect(x + 2, y + 2, rect_width - 4, rect_height - 4)
            cell = game.board[j * game.frame_width + i]
            if cell == ord('W'):
                pygame.draw.rect(surface, Colors.WALL_MAIN.value, rect)
                pygame.draw.rect(surface, Colors.WALL_BORDER.value, rect, 2)
                pygame.draw.line(surface, Colors.WALL_HIGHLIGHT.value,
                               (x + 2, y + 2), (x + rect_width - 2, y + 2), 2)
                pygame.draw.line(surface, Colors.WALL_HIGHLIGHT.value,
                               (x + 2, y + 2), (x + 2, y + rect_height - 2), 2)
            elif cell == ord('S'):
                pygame.draw.rect(surface, Colors.SNAKE_BODY.value, inner_rect, border_radius=6)
                highlight_rect = pygame.Rect(x + 4, y + 4, rect_width - 8, rect_height // 2 - 4)
                pygame.draw.rect(surface, Colors.SNAKE_BODY_LIGHT.value, highlight_rect, border_radius=4)
                pygame.draw.rect(surface, Colors.SNAKE_OUTLINE.value, inner_rect, 2, border_radius=6)
            elif cell == ord('R'):
                pygame.draw.circle(surface, Colors.RED_APPLE.value,
                                 (x + rect_width // 2, y + rect_height // 2),
                                 min(rect_width, rect_height) // 2 - 3)
                pygame.draw.circle(surface, Colors.RED_APPLE_DARK.value,
                                 (x + rect_width // 2 + 1, y + rect_height // 2 + 1),
                                 min(rect_width, rect_height) // 2 - 5)
                shine_x = x + rect_width // 2 - min(rect_width, rect_height) // 6
                shine_y = y + rect_height // 2 - min(rect_width, rect_height) // 6
                pygame.draw.circle(surface, Colors.RED_APPLE_SHINE.value,
                                 (shine_x, shine_y),
                                 min(rect_width, rect_height) // 8)
            elif cell == ord('G'):
                pygame.draw.circle(surface, Colors.GREEN_APPLE.value,
                                 (x + rect_width // 2, y + rect_height // 2),
                                 min(rect_width, rect_height) // 2 - 3)
                pygame.draw.circle(surface, Colors.GREEN_APPLE_DARK.value,
                                 (x + rect_width // 2 + 1, y + rect_height // 2 + 1),
                                 min(rect_width, rect_height) // 2 - 5)
                shine_x = x + rect_width // 2 - min(rect_width, rect_height) // 6
                shine_y = y + rect_height // 2 - min(rect_width, rect_height) // 6
                pygame.draw.circle(surface, Colors.GREEN_APPLE_SHINE.value,
                                 (shine_x, shine_y),
                                 min(rect_width, rect_height) // 7)
            elif cell == ord('H'):
                pygame.draw.rect(surface, Colors.SNAKE_HEAD.value, inner_rect, border_radius=8)
                gradient_rect = pygame.Rect(x + 4, y + rect_height // 2,
                                           rect_width - 8, rect_height // 2 - 2)
                pygame.draw.rect(surface, Colors.SNAKE_HEAD_DARK.value, gradient_rect, border_radius=6)
                pygame.draw.rect(surface, Colors.SNAKE_OUTLINE.value, inner_rect, 3, border_radius=8)
                eye_size = max(2, min(rect_width, rect_height) // 8)
                pygame.draw.circle(surface, (255, 255, 255),
                                 (x + rect_width // 3, y + rect_height // 3), eye_size)
                pygame.draw.circle(surface, (0, 0, 0),
                                 (x + rect_width // 3, y + rect_height // 3), eye_size - 1)
                pygame.draw.circle(surface, (255, 255, 255),
                                 (x + 2 * rect_width // 3, y + rect_height // 3), eye_size)
                pygame.draw.circle(surface, (0, 0, 0),
                                 (x + 2 * rect_width // 3, y + rect_height // 3), eye_size - 1)
