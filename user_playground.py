import pygame
from SnakeGame import SnakeGame, Directions, GameStatus
from utils import Colors, draw_board


def init_window(game: SnakeGame):
    pygame.init()
    surface: pygame.Surface = pygame.display.set_mode((550, 550))
    exit_game = False
    draw_board(surface, game)
    pygame.display.update()
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move_snake(Directions.UP)
                elif event.key == pygame.K_DOWN:
                    game.move_snake(Directions.DOWN)
                elif event.key == pygame.K_LEFT:
                    game.move_snake(Directions.LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.move_snake(Directions.RIGHT)
        draw_board(surface, game)
        if (game.status == GameStatus.GAME_OVER):
            surface.fill(Colors.BACKGROUND.value)
            font = pygame.font.SysFont(None, 55)
            text = font.render("GAME OVER", True, Colors.TEXT_GAME_OVER.value)
            text_rect = text.get_rect(center=(275, 225))
            surface.blit(text, text_rect)
        pygame.display.update()


if __name__ == "__main__":
    game = SnakeGame()
    # print("------------------ BOARD ------------------")
    # game.print_board()
    init_window(game)
