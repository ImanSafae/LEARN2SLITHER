import pygame
from Environment import Environment
from SnakeGame import GameStatus, SnakeGame
from utils import Colors, draw_board

class Interpreter:
    surface: pygame.Surface
    state: tuple
    reward: int
    terminated: bool

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((550, 550))
        # draw_board(self.surface, self.environment.game)
        pygame.display.update()

    def update(self, state: tuple, reward: int, terminated: bool, game: SnakeGame):
        self.state = state
        self.reward = reward
        self.terminated = terminated
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        draw_board(self.surface, game)
        if (game.status == GameStatus.GAME_OVER):
            self.surface.fill(Colors.WHITE.value)
            font = pygame.font.SysFont(None, 55)
            text = font.render("GAME OVER", True, Colors.RED.value)
            self.surface.blit(text, (175, 225))
        pygame.display.update()

    def get_step_result(self):
        return self.state, self.reward, self.terminated


