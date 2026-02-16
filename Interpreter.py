import pygame
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
            pygame.display.update()

    def init_pygame(self):
        pygame.init()
        self.surface = pygame.display.set_mode((550, 550))
        pygame.display.update()

    def _display_board(self, game: SnakeGame):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        draw_board(self.surface, game)
        if (game.status == GameStatus.GAME_OVER):
            overlay = pygame.Surface((550, 550))
            overlay.set_alpha(200)
            overlay.fill((255, 255, 255))

            self.surface.blit(overlay, (0, 0))
            font_title = pygame.font.SysFont('Arial', 65, bold=True)
            shadow = font_title.render("GAME OVER", True, Colors.TEXT_SHADOW.value)
            self.surface.blit(shadow, (157, 227))
            text = font_title.render("GAME OVER", True, Colors.TEXT_GAME_OVER.value)
            self.surface.blit(text, (155, 225))

            score = len(game.snake)
            font_score = pygame.font.SysFont('Arial', 40, bold=False)
            score_text = f"Score: {score}"
            shadow_score = font_score.render(score_text, True, Colors.TEXT_SHADOW.value)
            self.surface.blit(shadow_score, (202, 302))
            text_score = font_score.render(score_text, True, (50, 50, 50))
            self.surface.blit(text_score, (200, 300))
        elif (game.status == GameStatus.VICTORY):
            overlay = pygame.Surface((550, 550))
            overlay.set_alpha(200)
            overlay.fill((255, 255, 255))
            self.surface.blit(overlay, (0, 0))

            font_title = pygame.font.SysFont('Arial', 70, bold=True)
            shadow = font_title.render("VICTORY!", True, Colors.TEXT_SHADOW.value)
            self.surface.blit(shadow, (157, 227))
            text = font_title.render("VICTORY!", True, Colors.TEXT_VICTORY.value)
            self.surface.blit(text, (155, 225))

            score = len(game.snake)
            font_score = pygame.font.SysFont('Arial', 40, bold=False)
            score_text = f"Score: {score}"
            shadow_score = font_score.render(score_text, True, Colors.TEXT_SHADOW.value)
            self.surface.blit(shadow_score, (202, 302))
            text_score = font_score.render(score_text, True, (50, 50, 50))
            self.surface.blit(text_score, (200, 300))

            for _ in range(20):
                import random
                x = random.randint(50, 500)
                y = random.randint(50, 200)
                size = random.randint(3, 8)
                color = random.choice([
                    Colors.TEXT_VICTORY.value,
                    Colors.GREEN_APPLE_SHINE.value,
                    (255, 215, 0),
                    (255, 182, 193)
                ])
                pygame.draw.circle(self.surface, color, (x, y), size)
        pygame.display.update()

    def update(self, state: tuple, reward: int, terminated: bool, game: SnakeGame):
        self.state = state
        self.reward = reward
        self.terminated = terminated
        if self.display_mode:
            self._display_board(game)

    def get_step_result(self):
        return self.state, self.reward, self.terminated
