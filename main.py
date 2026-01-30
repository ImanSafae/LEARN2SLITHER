import pygame
from snake.Game import Game, Directions, GameStatus
from enum import Enum

class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    PURPLE = (128, 0, 128)
    
def draw_board(surface: pygame.Surface, game: Game):
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

def init_window(game: Game):
    pygame.init()
    surface: pygame.Surface = pygame.display.set_mode((550, 550))

    exit_game = False
    draw_board(surface, game)
    # surface.fill(Colors.WHITE.value)
    # rect_width = 500 // game.frame_width
    # rect_height = 500 // game.frame_height
    # rect = pygame.Rect(25, 25, rect_width, rect_height)
    # pygame.draw.rect(surface, Colors.BLACK.value, rect, width=1)
    # for j in range(game.frame_height):
    #     for i in range(game.frame_width):
    #         rect = pygame.Rect(25 + i * rect_width, 25 + j * rect_height, rect_width, rect_height)
    #         if game.board[j * game.frame_width + i] == ord('W'):
    #             pygame.draw.rect(surface, Colors.PURPLE.value, rect)
    #         elif game.board[j * game.frame_width + i] == ord('S'):
    #             pygame.draw.rect(surface, Colors.BLACK.value, rect)
    #         elif game.board[j * game.frame_width + i] == ord('R'):
    #             pygame.draw.rect(surface, Colors.RED.value, rect)
    #         elif game.board[j * game.frame_width + i] == ord('G'):
    #             pygame.draw.rect(surface, Colors.GREEN.value, rect)
    #         elif game.board[j * game.frame_width + i] == ord('H'):
    #             pygame.draw.rect(surface, Colors.BLACK.value, rect, width=10)
    #         else:
    #             pygame.draw.rect(surface, Colors.BLACK.value, rect, width=1)
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
                # pygame.display.update()
        if (game.status == GameStatus.GAME_OVER):
            surface.fill(Colors.WHITE.value)
            font = pygame.font.SysFont(None, 55)
            text = font.render("GAME OVER", True, Colors.RED.value)
            surface.blit(text, (175, 225))
        pygame.display.update()

if __name__ == "__main__":
    game = Game()
    # print("------------------ BOARD ------------------")
    # game.print_board()
    init_window(game)