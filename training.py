
from Agent import Agent
from Interpreter import Interpreter
from SnakeGame import SnakeGame
from Environment import Environment


if __name__ == "__main__":
    game = SnakeGame()
    interpreter = Interpreter()
    environment = Environment(game, interpreter)
    agent = Agent(environment, interpreter)
    agent.train(episodes=1000)