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

    fw = game.frame_width
    fh = game.frame_height
    rw = rect_width
    rh = rect_height
    for j in range(fh):
        for i in range(fw):
            x = 25 + i * rw
            y = 25 + j * rh
            rect = pygame.Rect(x, y, rw, rh)
            idx = j * fw + i
            if game.board[idx] != ord('W'):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(
                        surface,
                        Colors.GRID_LIGHT.value,
                        rect)
                else:
                    pygame.draw.rect(
                        surface,
                        Colors.GRID_DARK.value,
                        rect)
    for j in range(fh):
        for i in range(fw):
            x = 25 + i * rw
            y = 25 + j * rh
            rect = pygame.Rect(x, y, rw, rh)
            inner = pygame.Rect(
                x + 2, y + 2, rw - 4, rh - 4)
            cell = game.board[j * fw + i]
            cx = x + rw // 2
            cy = y + rh // 2
            ms = min(rw, rh)
            if cell == ord('W'):
                pygame.draw.rect(
                    surface,
                    Colors.WALL_MAIN.value, rect)
                pygame.draw.rect(
                    surface,
                    Colors.WALL_BORDER.value,
                    rect, 2)
                whl = Colors.WALL_HIGHLIGHT.value
                pygame.draw.line(
                    surface, whl,
                    (x + 2, y + 2),
                    (x + rw - 2, y + 2), 2)
                pygame.draw.line(
                    surface, whl,
                    (x + 2, y + 2),
                    (x + 2, y + rh - 2), 2)
            elif cell == ord('S'):
                pygame.draw.rect(
                    surface,
                    Colors.SNAKE_BODY.value,
                    inner, border_radius=6)
                hl_rect = pygame.Rect(
                    x + 4, y + 4,
                    rw - 8, rh // 2 - 4)
                pygame.draw.rect(
                    surface,
                    Colors.SNAKE_BODY_LIGHT.value,
                    hl_rect, border_radius=4)
                pygame.draw.rect(
                    surface,
                    Colors.SNAKE_OUTLINE.value,
                    inner, 2, border_radius=6)
            elif cell == ord('R'):
                pygame.draw.circle(
                    surface,
                    Colors.RED_APPLE.value,
                    (cx, cy), ms // 2 - 3)
                pygame.draw.circle(
                    surface,
                    Colors.RED_APPLE_DARK.value,
                    (cx + 1, cy + 1),
                    ms // 2 - 5)
                sx = cx - ms // 6
                sy = cy - ms // 6
                pygame.draw.circle(
                    surface,
                    Colors.RED_APPLE_SHINE.value,
                    (sx, sy), ms // 8)
            elif cell == ord('G'):
                pygame.draw.circle(
                    surface,
                    Colors.GREEN_APPLE.value,
                    (cx, cy), ms // 2 - 3)
                pygame.draw.circle(
                    surface,
                    Colors.GREEN_APPLE_DARK.value,
                    (cx + 1, cy + 1),
                    ms // 2 - 5)
                sx = cx - ms // 6
                sy = cy - ms // 6
                pygame.draw.circle(
                    surface,
                    Colors.GREEN_APPLE_SHINE.value,
                    (sx, sy), ms // 7)
            elif cell == ord('H'):
                pygame.draw.rect(
                    surface,
                    Colors.SNAKE_HEAD.value,
                    inner, border_radius=8)
                grad = pygame.Rect(
                    x + 4, y + rh // 2,
                    rw - 8, rh // 2 - 2)
                pygame.draw.rect(
                    surface,
                    Colors.SNAKE_HEAD_DARK.value,
                    grad, border_radius=6)
                pygame.draw.rect(
                    surface,
                    Colors.SNAKE_OUTLINE.value,
                    inner, 3, border_radius=8)
                es = max(2, ms // 8)
                ex1 = x + rw // 3
                ex2 = x + 2 * rw // 3
                ey = y + rh // 3
                pygame.draw.circle(
                    surface, (255, 255, 255),
                    (ex1, ey), es)
                pygame.draw.circle(
                    surface, (0, 0, 0),
                    (ex1, ey), es - 1)
                pygame.draw.circle(
                    surface, (255, 255, 255),
                    (ex2, ey), es)
                pygame.draw.circle(
                    surface, (0, 0, 0),
                    (ex2, ey), es - 1)
