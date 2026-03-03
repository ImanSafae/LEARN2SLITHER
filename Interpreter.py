import pygame
from SnakeGame import GameStatus, SnakeGame
from utils import Colors, draw_board


class Interpreter:
    surface: pygame.Surface
    state: tuple
    reward: int
    terminated: bool
    display_mode: bool
    step_by_step: bool
    next_step_clicked: bool
    max_length: int

    def __init__(self, display_mode=True, step_by_step=False):
        self.display_mode = display_mode
        self.step_by_step = step_by_step
        self.next_step_clicked = False
        self.state = None
        self.reward = 0
        self.terminated = False
        self.max_length = 0
        if self.display_mode:
            pygame.init()
            self.surface = pygame.display.set_mode((550, 550))
            pygame.display.update()

    def init_pygame(self):
        pygame.init()
        self.surface = pygame.display.set_mode((550, 550))
        pygame.display.update()

    def _draw_next_button(self):
        button_rect = pygame.Rect(450, 500, 90, 40)
        button_color = (50, 150, 50)
        pygame.draw.rect(self.surface, button_color,
                         button_rect, border_radius=5)
        pygame.draw.rect(self.surface, (200, 200, 200),
                         button_rect, 2, border_radius=5)
        font_button = pygame.font.SysFont('Arial', 16, bold=True)
        button_text = font_button.render("NEXT", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.surface.blit(button_text, button_text_rect)
        return button_rect

    def wait_for_next(self, game: SnakeGame):
        """Draw board and block until NEXT is clicked."""
        draw_board(self.surface, game)
        self.next_step_clicked = False
        while not self.next_step_clicked:
            next_button_rect = self._draw_next_button()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_button_rect.collidepoint(
                        event.pos
                    ):
                        self.next_step_clicked = True

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
            shadow = font_title.render(
                "GAME OVER", True, Colors.TEXT_SHADOW.value)
            shadow_rect = shadow.get_rect(center=(275, 227))
            self.surface.blit(shadow, shadow_rect)
            text = font_title.render(
                "GAME OVER", True, Colors.TEXT_GAME_OVER.value)
            text_rect = text.get_rect(center=(275, 225))
            self.surface.blit(text, text_rect)

            score = len(game.snake)
            if score > self.max_length:
                self.max_length = score
            font_score = pygame.font.SysFont('Arial', 40, bold=False)
            score_text = f"Score: {score}"
            stats_text = f"Max length: {self.max_length}"
            shadow_score = font_score.render(
                score_text, True, Colors.TEXT_SHADOW.value)
            shadow_score_rect = shadow_score.get_rect(center=(275, 302))
            self.surface.blit(shadow_score, shadow_score_rect)
            text_score = font_score.render(score_text, True, (50, 50, 50))
            text_stats = font_score.render(stats_text, True, (50, 50, 50))
            text_score_rect = text_score.get_rect(center=(275, 300))
            self.surface.blit(text_score, text_score_rect)
            text_stats_rect = text_stats.get_rect(center=(275, 340))
            self.surface.blit(text_stats, text_stats_rect)
        elif (game.status == GameStatus.VICTORY):
            overlay = pygame.Surface((550, 550))
            overlay.set_alpha(200)
            overlay.fill((255, 255, 255))
            self.surface.blit(overlay, (0, 0))

            font_title = pygame.font.SysFont('Arial', 70, bold=True)
            shadow = font_title.render(
                "VICTORY!", True, Colors.TEXT_SHADOW.value)
            shadow_rect = shadow.get_rect(center=(275, 227))
            self.surface.blit(shadow, shadow_rect)
            text = font_title.render(
                "VICTORY!", True, Colors.TEXT_VICTORY.value)
            text_rect = text.get_rect(center=(275, 225))
            self.surface.blit(text, text_rect)

            score = len(game.snake)
            font_score = pygame.font.SysFont('Arial', 40, bold=False)
            score_text = f"Score: {score}"
            shadow_score = font_score.render(
                score_text, True, Colors.TEXT_SHADOW.value)
            shadow_score_rect = shadow_score.get_rect(
                center=(275, 302))
            self.surface.blit(shadow_score, shadow_score_rect)
            text_score = font_score.render(score_text, True, (50, 50, 50))
            text_score_rect = text_score.get_rect(center=(275, 300))
            self.surface.blit(text_score, text_score_rect)

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

    def update(self, state: tuple, reward: int,
               terminated: bool, game: SnakeGame,
               step_by_step: bool = False):
        self.state = state
        self.reward = reward
        self.terminated = terminated
        self.step_by_step = step_by_step
        if self.display_mode:
            self._display_board(game)

    def show_exploit_summary(self, scores: list):
        if not self.display_mode:
            return
        if not scores:
            scores = [0]

        recent_scores = scores[-10:]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

            if not running:
                break

            self.surface.fill((240, 248, 255))

            title_font = pygame.font.SysFont('Arial', 40, bold=True)
            title = title_font.render("SCORES", True, Colors.SNAKE_HEAD.value)
            title_rect = title.get_rect(center=(275, 50))
            self.surface.blit(title, title_rect)

            score_font = pygame.font.SysFont('Arial', 24)
            y_offset = 105
            for index, score in enumerate(recent_scores, start=1):
                line = score_font.render(
                    f"Game {index}: {score}",
                    True, (50, 50, 50))
                line_rect = line.get_rect(center=(275, y_offset))
                self.surface.blit(line, line_rect)
                y_offset += 32

            max_font = pygame.font.SysFont('Arial', 30, bold=True)
            max_text = max_font.render(
                f"Max length: {self.max_length}",
                True, Colors.SNAKE_OUTLINE.value)
            max_rect = max_text.get_rect(center=(275, 470))
            self.surface.blit(max_text, max_rect)

            hint_font = pygame.font.SysFont('Arial', 18)
            hint_text = hint_font.render(
                "Close the window to exit",
                True, (90, 90, 90))
            hint_rect = hint_text.get_rect(center=(275, 500))
            self.surface.blit(hint_text, hint_rect)

            pygame.display.update()

    def get_step_result(self):
        return self.state, self.reward, self.terminated
