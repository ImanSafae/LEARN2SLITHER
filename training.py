
from Agent import Agent
from Interpreter import Interpreter
from SnakeGame import SnakeGame
from Environment import Environment
import matplotlib.pyplot as plt
import numpy as np
import pickle

def plot_lengths(lengths_history):
    plt.plot(lengths_history)
    plt.xlabel('Episode')
    plt.ylabel('Snake Length at Game Over')
    plt.title('Snake Length at Game Over Over Episodes')
    plt.show()

def export_q_table(q_table: dict):
    # np.savetxt("q_table.csv", q_table, delimiter=",")
    with open("q_table.pkl", "wb") as f:
        pickle.dump(q_table, f)


if __name__ == "__main__":
    game = SnakeGame()
    interpreter = Interpreter(display_mode=False)
    environment = Environment(game, interpreter, max_steps=400)
    agent = Agent(environment, interpreter, 
                  learning_rate=0.25,
                  epsilon=1.0,
                  decay_rate=0.9995,
                  discount=0.95)
    
    print("=== TRAINING ===")
    agent.train(episodes=5000)
    print("\n=== RESULTS OVER TRAINING ===")
    print(f"Q-table length: {len(agent.q_table)}")
    print(f"Max snake length: {max(agent.lengths_history)}")
    print(f"Avg snake length: {sum(agent.lengths_history)/len(agent.lengths_history):.2f}")
    
    
    # Pure exploitation
    print("\n=== PURE EXPLOITATION TEST (epsilon=0) ===")
    agent.epsilon = 0.0
    interpreter.display_mode = True
    agent.sleep_time = 1.0
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
    export_q_table(agent.q_table)