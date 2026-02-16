
from Agent import Agent
from Interpreter import Interpreter
from SnakeGame import SnakeGame
from Environment import Environment
import matplotlib.pyplot as plt
import pickle
from argparse import ArgumentParser
import pygame
from utils import Colors


def show_start_screen(mode: str):
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Snake Training")
    button_rect = pygame.Rect(200, 300, 200, 60)
    running = True
    while running:
        screen.fill((240, 248, 255))
        font_title = pygame.font.SysFont('Arial', 60, bold=True)
        title = font_title.render("LEARN 2 SLITHER", True, Colors.SNAKE_HEAD.value)
        title_rect = title.get_rect(center=(300, 100))
        screen.blit(title, title_rect)
        font_subtitle = pygame.font.SysFont('Arial', 24)
        subtitle = font_subtitle.render(f"{mode} Mode", True, (100, 100, 100))
        subtitle_rect = subtitle.get_rect(center=(300, 160))
        screen.blit(subtitle, subtitle_rect)
        if mode == "Training":
            info_text = [
                "The agent will learn to play Snake",
                "using reinforcement learning",
                "This may take a few minutes..."
            ]
        else:
            info_text = [
                "The agent will play Snake",
                "using the learned Q-table",
                "No training will occur."
            ]
        y_offset = 210
        font_info = pygame.font.SysFont('Arial', 18)
        for text in info_text:
            rendered = font_info.render(text, True, (80, 80, 80))
            text_rect = rendered.get_rect(center=(300, y_offset))
            screen.blit(rendered, text_rect)
            y_offset += 30
        mouse_pos = pygame.mouse.get_pos()
        is_hover = button_rect.collidepoint(mouse_pos)
        button_color = Colors.SNAKE_HEAD.value if is_hover else Colors.SNAKE_BODY.value
        pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
        pygame.draw.rect(screen, Colors.SNAKE_OUTLINE.value, button_rect, 3, border_radius=10)
        font_button = pygame.font.SysFont('Arial', 32, bold=True)
        button_text = font_button.render("START", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.quit()
                    return True
        pygame.display.flip()
    return False


def plot_lengths(lengths_history):
    plt.plot(lengths_history)
    plt.xlabel('Episode')
    plt.ylabel('Snake Length at Game Over')
    plt.title('Snake Length at Game Over Over Episodes')
    plt.show()


def export_params(q_table: dict, game: SnakeGame):
    with open("q_table.pkl", "wb") as f:
        pickle.dump(q_table, f)


def exploit(args: ArgumentParser):
    if not show_start_screen("Exploit"):
        print("Exploitation cancelled by user")
        return
    if args.step_by_step:
        sleep_time = 0.5
    else:
        sleep_time = 0.0
    q_table: dict = pickle.load(open("q_table.pkl", "rb"))
    interpreter = Interpreter(display_mode=True)
    environment = Environment(None, interpreter, max_steps=400)
    agent = Agent(environment, interpreter)
    agent.exploit(q_table, sleep_time=sleep_time)


def train(args: ArgumentParser):
    if args.display:
        if not show_start_screen("Training"):
            print("Training cancelled by user")
            return
    if args.step_by_step:
        sleep_time = 0.5
    else:
        sleep_time = 0.0
    game = SnakeGame(width=args.width, height=args.height)
    interpreter = Interpreter(display_mode=args.display)
    environment = Environment(game, interpreter, max_steps=400)
    agent = Agent(environment, interpreter,
                  learning_rate=0.25,
                  epsilon=1.0,
                  decay_rate=0.9995,
                  discount=0.95)
    agent.sleep_time = sleep_time if (args.step_by_step and args.display) else None

    print("=== TRAINING ===")
    agent.train(episodes=args.episodes)
    print("\n=== RESULTS OVER TRAINING ===")
    print(f"Q-table length: {len(agent.q_table)}")
    print(f"Max snake length: {max(agent.lengths_history)}")
    print(f"Avg snake length: {sum(agent.lengths_history)/len(agent.lengths_history):.2f}")

    # Pure exploitation
    print("\n=== PURE EXPLOITATION TEST (epsilon=0) ===")
    agent.epsilon = 0.0
    interpreter.display_mode = True
    agent.sleep_time = 1.0 if args.step_by_step else 0.0
    test_lengths = []
    interpreter.init_pygame()
    for i in range(10):
        agent.environment.reset()
        while not agent.environment.terminated:
            state = agent.environment.state
            action = agent.choose_action(state)
            agent.environment.step(action)
        test_lengths.append(len(agent.environment.game.snake))

    print(f"Test avg length: {sum(test_lengths)/len(test_lengths):.2f}")
    print(f"Test max length: {max(test_lengths)}")
    print(f"Test min length: {min(test_lengths)}")
    plot_lengths(agent.lengths_history)
    export_params(agent.q_table, game)


if __name__ == "__main__":
    parser = ArgumentParser(description="Train a Q-learning agent to play Snake")
    parser.add_argument("--episodes", type=int, default=5000, help="Number of training episodes")
    parser.add_argument("--width", "-w", type=int, default=10, help="Width of the game board")
    parser.add_argument("--height", "-H", type=int, default=10, help="Height of the game board")
    parser.add_argument("-display", action="store_true", help="Display the game during training")
    parser.add_argument("-train", action="store_true", help="Run training (default)")
    parser.add_argument("-exploit", action="store_true", help="Run pure exploitation test after training")
    parser.add_argument("-step-by-step", action="store_true", help="Run pure exploitation test in step-by-step mode")
    args = parser.parse_args()

    if args.exploit:
        exploit(args)
        exit(0)
    else:
        train(args)
        exit(0)
