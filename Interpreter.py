import pygame
from Agent import Agent
from Environment import Environment
from SnakeGame import SnakeGame, Directions, GameStatus
from utils import Colors, draw_board

class Interpreter:
    agent: Agent
    environment: Environment
    surface: pygame.Surface

    def __init__(self, agent: Agent, environment: Environment):
        self.agent = agent
        self.environment = environment
        pygame.init()
        self.surface = pygame.display.set_mode((550, 550))
        draw_board(self.surface, self.environment.game)
        pygame.display.update()

    def update(self, state: tuple, reward: int, terminated: bool):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        draw_board(self.surface, self.environment.game)
        if (self.environment.game.status == GameStatus.GAME_OVER):
            self.surface.fill(Colors.WHITE.value)
            font = pygame.font.SysFont(None, 55)
            text = font.render("GAME OVER", True, Colors.RED.value)
            self.surface.blit(text, (175, 225))
        pygame.display.update()

    def get_step_result(self):
        return self.environment.state, self.environment.last_reward, self.environment.terminated


