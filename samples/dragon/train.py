import numpy as np
from tensorflow.keras.models import load_model
import os
import random

from src.agent import QLearningAgent
from src.tictactoe import TicTacToe

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
            game.dumpBoard()

        else:
            print(f"{prefix} > {name}: Invalid move at position {position}! | State: {game.board}")

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
        print(f"{prefix} > Nobody wins in this turn, play another one. Agent's reward is: 0")
        agent.step(boardToState(game.board), 0)

    print(f'{prefix} > Game over! Winner: {game.winner}')

# -------------------------------------------------------------------------------------------

agent = QLearningAgent()
if os.path.exists('trained_model.keras'):
    agent.model = load_model('trained_model.keras')

opponent = QLearningAgent(exploration_rate=1.0)  # The opponent is more exploratory and always chooses random actions

numberOfGames = 100
for numGame in range(numberOfGames):
    prefix = f"{numGame+1}/{numberOfGames}"

    # Play each game
    print(f"Playing game {prefix}...")
    playGame(prefix, agent, opponent)
    print()

    # Save after every play, to allow cancel the script at any time
    agent.model.save('trained_model.keras')
