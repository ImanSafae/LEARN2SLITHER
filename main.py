
from Agent import Agent
from Interpreter import Interpreter
from SnakeGame import SnakeGame
from Environment import Environment
import matplotlib.pyplot as plt
import pickle
from argparse import ArgumentParser
import pygame
from utils import Colors
import time


def show_start_screen(mode: str):
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Snake Training")
    button_rect = pygame.Rect(200, 300, 200, 60)
    running = True
    while running:
        screen.fill((240, 248, 255))
        font_title = pygame.font.SysFont(
            'Arial', 60, bold=True)
        title = font_title.render(
            "LEARN 2 SLITHER", True,
            Colors.SNAKE_HEAD.value)
        title_rect = title.get_rect(
            center=(300, 100))
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
        button_color = (
            Colors.SNAKE_HEAD.value
            if is_hover
            else Colors.SNAKE_BODY.value)
        pygame.draw.rect(
            screen, button_color,
            button_rect, border_radius=10)
        pygame.draw.rect(
            screen, Colors.SNAKE_OUTLINE.value,
            button_rect, 3, border_radius=10)
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
    elif args.readable:
        sleep_time = 0.25
    else:
        sleep_time = 0.0
    path = args.path if args.path else "q_table.pkl"
    with open(path, "rb") as f:
        q_table: dict = pickle.load(f)
    interpreter = Interpreter(
        display_mode=True,
        step_by_step=args.step_by_step)
    environment = Environment(
        None, interpreter, max_steps=400,
        step_by_step=args.step_by_step)
    agent = Agent(
        environment, interpreter,
        step_by_step=args.step_by_step,
        print_actions_mode=args.verbose)
    agent.exploit(q_table, sleep_time=sleep_time)


def train(args: ArgumentParser):
    sleep_time = 0.0
    if args.step_by_step:
        sleep_time = 0.5
    elif args.readable:
        sleep_time = 0.25
    if args.display:
        if not show_start_screen("Training"):
            print("Training cancelled by user")
            return
    game = SnakeGame(width=args.width, height=args.height)
    step_by_step_flag = (args.step_by_step
                         if args.display else False)
    interpreter = Interpreter(display_mode=args.display,
                              step_by_step=step_by_step_flag)
    environment = Environment(game, interpreter, max_steps=400,
                              step_by_step=step_by_step_flag)
    agent = Agent(environment, interpreter,
                  learning_rate=0.25,
                  epsilon=0.8,
                  decay_rate=0.995,
                  discount=0.95,
                  step_by_step=step_by_step_flag,
                  print_actions_mode=args.verbose)
    agent.sleep_time = sleep_time if (args.display) else None

    print("=== TRAINING ===")
    agent.train(episodes=args.episodes)
    print("\n=== RESULTS OVER TRAINING ===")
    print(f"Q-table length: {len(agent.q_table)}")
    print(f"Max snake length: {max(agent.lengths_history)}")
    print(f"Avg snake length: "
          f"{sum(agent.lengths_history)/len(agent.lengths_history):.2f}")

    # stats in pure exploitation
    print("\n=== PURE EXPLOITATION TEST (epsilon=0) ===")
    agent.epsilon = 0.0
    interpreter.display_mode = True
    agent.sleep_time = sleep_time
    test_lengths = []
    interpreter.init_pygame()
    for i in range(20):
        agent.environment.reset()
        while not agent.environment.terminated:
            state = agent.environment.state
            action = agent.choose_action(state)
            agent.environment.step(action)
            time.sleep(agent.sleep_time if agent.sleep_time else 0)
        test_lengths.append(len(agent.environment.game.snake))

    print(f"Test avg length: "
          f"{sum(test_lengths)/len(test_lengths):.2f}")
    print(f"Test max length: {max(test_lengths)}")
    print(f"Test min length: {min(test_lengths)}")
    plot_lengths(agent.lengths_history)
    export_params(agent.q_table, game)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Train a Q-learning agent"
    )
    parser.add_argument(
        "--episodes", type=int, default=6000,
        help="Number of training episodes")
    parser.add_argument(
        "--width", "-w", type=int, default=10,
        help="Width of the game board")
    parser.add_argument(
        "--height", "-H", type=int, default=10,
        help="Height of the game board")
    parser.add_argument(
        "-display", action="store_true",
        help="Display the game during training")
    parser.add_argument(
        "-train", action="store_true",
        help="Run training (default)")
    parser.add_argument(
        "-exploit", action="store_true",
        help="Run exploitation test")
    parser.add_argument(
        "-step-by-step", action="store_true",
        help="Run in step-by-step mode")
    parser.add_argument(
        "-readable", action="store_true",
        help="Readable mode with delays",
        default=False)
    parser.add_argument(
        "-verbose", action="store_true",
        help="Print chosen actions during training and exploitation",
        default=False)
    parser.add_argument("-path", type=str, default="q_table.pkl",
                        help="Path to Q-table for exploitation")
    args = parser.parse_args()

    try:
        if args.exploit:
            exploit(args)
            exit(0)
        else:
            train(args)
            exit(0)
    except Exception as e:
        print("An error occurred:", e)
        exit(1)
