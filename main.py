import pygame
from snake.Game import Game
from enum import Enum

class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)



def init_window(game: Game):
    pygame.init()
    surface: pygame.Surface = pygame.display.set_mode((550, 550))

    exit_game = False
    surface.fill(Colors.WHITE.value)
    rect_width = 500 // game.frame_width
    rect_height = 500 // game.frame_height
    rect = pygame.Rect(25, 25, rect_width, rect_height)
    pygame.draw.rect(surface, Colors.BLACK.value, rect, width=1)
    for j in range(game.frame_height):
        for i in range(game.frame_width):
            rect = pygame.Rect(25 + i * rect_width, 25 + j * rect_height, rect_width, rect_height)
            pygame.draw.rect(surface, Colors.BLACK.value, rect, width=1)
    pygame.display.update()
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True


        # pygame.display.update()

if __name__ == "__main__":
    game = Game()
    print("------------------ BOARD ------------------")
    game.print_board()
    init_window(game)