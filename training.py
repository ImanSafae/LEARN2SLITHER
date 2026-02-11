
from Agent import Agent
from Interpreter import Interpreter
from SnakeGame import SnakeGame
from Environment import Environment
import matplotlib.pyplot as plt

def plot_lengths(lengths_history):
    plt.plot(lengths_history)
    plt.xlabel('Episode')
    plt.ylabel('Snake Length at Game Over')
    plt.title('Snake Length at Game Over Over Episodes')
    plt.show()

if __name__ == "__main__":
    game = SnakeGame()
    interpreter = Interpreter()
    environment = Environment(game, interpreter)
    agent = Agent(environment, interpreter)
    agent.train(episodes=1000)
    print("q-table after training:", len(agent.q_table))
    plot_lengths(agent.lengths_history)