
from Agent import Agent
from SnakeGame import SnakeGame
from Environment import Environment


if __name__ == "__main__":
    game = SnakeGame()
    environment = Environment(game)
    agent = Agent(environment)
    agent.train(episodes=1000)