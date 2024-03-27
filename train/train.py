import numpy as np
from tensorflow.keras.models import load_model
import tensorflow
import os
import random
import sys

from agent import QLearningAgent
from tictactoe import TicTacToe

# -------------------------------------------------------------------------------------------

def boardToState(board):
    state = []

    for cell in board:
        if cell == 'E':
            state.append(0)
        elif cell == 'X':
            state.append(1)
        elif cell == 'O':
            state.append(-1)

    return state

# -------------------------------------------------------------------------------------------

def agentPlay(prefix, name, game, agent, symbol):
    validMove = False
    while not validMove:
        position = agent.start(boardToState(game.board))
        
        validMove = game.makeMove(symbol, position)
        if validMove:
            print(f"{prefix} > {name}: Plays {symbol} at position {position} | State: {game.board}")

    return game.checkGameOver()

# -------------------------------------------------------------------------------------------

def playGame(prefix, agent, opponent):
    emptyBoard = "EEEEEEEEE"

    game = TicTacToe(emptyBoard)

    # Choose who starts the game
    agentIsO = random.choice([True, False])
    print(f"{prefix} > NOTE: In this game the agent is {'O' if agentIsO else 'X'}")

    while not game.checkGameOver() and not game.noPossibleMove():
        if agentIsO:
            # Give an immediate reward on 1 if the agent wins
            position = agentPlay(prefix, "Agent", game, agent, 'O')
            if game.checkGameOver():
                print(f"{prefix} > Agent wins! Agent's reward is: +1")
                agent.learn(boardToState(game.board), position, 1, None)
                break

            # Give an immediate penalty regard on -1 if the opponent wins
            position = agentPlay(prefix, "Opponent", game, opponent, 'X')
            if game.checkGameOver():
                print(f"{prefix} > Opponent wins! Agent's reward is: -1")
                agent.learn(boardToState(game.board), position, -1, None)
                break

        else:
            # Give an immediate penalty regard on -1 if the opponent wins
            position = agentPlay(prefix, "Opponent", game, opponent, 'O')
            if game.checkGameOver():
                print(f"{prefix} > Opponent wins! Agent's reward is: -1")
                agent.learn(boardToState(game.board), position, -1, None)
                break

            # Give an immediate reward on 1 if the agent wins
            position = agentPlay(prefix, "Agent", game, agent, 'X')
            if game.checkGameOver():
                print(f"{prefix} > Agent wins! Agent's reward is: +1")
                agent.learn(boardToState(game.board), position, 1, None)
                break

        # If no one wins, give a reward of 0
        agent.step(boardToState(game.board), 0)

    print(f'{prefix} > Game over! Winner: {game.winner}')
    game.dumpBoard()

    if (agentIsO and game.winner == 'O') or (not agentIsO and game.winner == 'X'):
        return 1
    elif game.winner == 'D':
        return 0
    else:
        return -1

# -------------------------------------------------------------------------------------------

# Reopen the trained model if available
agent = QLearningAgent()
if os.path.exists('dragon.keras'):
    agent.model = load_model('dragon.keras')

# The opponent muest be more exploratory; set yo 1.o to always choose random actions
# exploration_rate goes from 0.0 to 1.0)
opponent = QLearningAgent(exploration_rate=0.8)  

# We can optionally set the number of games from command line
try:
    numberOfGames = int(sys.argv[1])
except:
    numberOfGames = 10

# Uncomment to disable keras training messages
tensorflow.keras.utils.disable_interactive_logging()

# Play each game
wins = 0
draws = 0
loses = 0

for numGame in range(numberOfGames):
    prefix = f"{numGame+1}/{numberOfGames}"

    print(f"Playing game {prefix}...")
    result = playGame(prefix, agent, opponent)

    if result == 1:
        wins += 1
    elif result == 0:
        draws += 1
    else:
        loses += 1

    print(f'{prefix} > Training result until now: {wins} wins, {loses} loses, {draws} draws')
    print()

# Save the trained model
print(f'Final training result: {wins} wins, {loses} loses, {draws} draws')
agent.model.save('dragon.keras')

print()
