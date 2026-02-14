import pygame
from Environment import Environment
from SnakeGame import GameStatus, SnakeGame
from utils import Colors, draw_board

class Interpreter:
    surface: pygame.Surface
    state: tuple
    reward: int
    terminated: bool
    display_mode: bool

    def __init__(self, display_mode=True):
        self.display_mode = display_mode
        self.state = None
        self.reward = 0
        self.terminated = False
        if self.display_mode:
            pygame.init()
            self.surface = pygame.display.set_mode((550, 550))
        # draw_board(self.surface, self.environment.game)
            pygame.display.update()

    def init_pygame(self):
        pygame.init()
        self.surface = pygame.display.set_mode((550, 550))
        # draw_board(self.surface, self.environment.game)
        pygame.display.update()

    def _display_board(self, game: SnakeGame):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        draw_board(self.surface, game)
        if (game.status == GameStatus.GAME_OVER):
            self.surface.fill(Colors.WHITE.value)
            font = pygame.font.SysFont(None, 55)
            text = font.render("GAME OVER", True, Colors.RED.value)
            self.surface.blit(text, (175, 225))
        elif (game.status == GameStatus.VICTORY):
            self.surface.fill(Colors.WHITE.value)
            font = pygame.font.SysFont(None, 55)
            text = font.render("VICTORY!", True, Colors.GREEN.value)
            self.surface.blit(text, (175, 225))
        pygame.display.update()

    def update(self, state: tuple, reward: int, terminated: bool, game: SnakeGame):
        self.state = state
        self.reward = reward
        self.terminated = terminated
        if self.display_mode:
            self._display_board(game)

    def get_step_result(self):
        return self.state, self.reward, self.terminated


