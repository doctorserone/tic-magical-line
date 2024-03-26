import numpy as np
import tensorflow as tf
import os

# -------------------------------------------------------------------------------------------

'''

Tic-Tac-Toe is a great example to understand Q-learning! Here's a breakdown of how it works in this context:

Components:

State: The current board configuration represented as a list or array (e.g., [" ", "X", " ", "O", " ", "X", " ", " ", " "]).
Action: A possible move the AI can take (e.g., placing its mark at a specific position on the board).
Reward: A numerical value assigned to an outcome. (e.g., +1 for winning, -1 for losing, 0 for ongoing game).
Q-table: A 2D table that stores the estimated Q-value for each state-action pair. The Q-value represents the expected future reward of taking a specific action in a particular state.
Learning Process:

Initialization: The Q-table is initially filled with zeros or random values.

Playing Games: The AI plays multiple games against itself (or another player).

Taking Actions: At each state, the AI:

Explores: Sometimes, it might choose a random action to explore the state space.
Exploits: Other times, it chooses the action with the highest Q-value in the current state (exploitation).
Updating Q-values: After taking an action and observing the resulting reward (and next state), the Q-value for the previous state-action pair is updated using the Bellman equation:

Q(s, a) <- Q(s, a) + α ( R(s, a) + γ * max(Q(s', a')) )
where:

α (alpha) is the learning rate (between 0 and 1).
γ (gamma) is the discount factor (between 0 and 1).
R(s, a) is the reward received for taking action a in state s.
max(Q(s', a')) is the maximum Q-value achievable from the next state s' (considering all possible actions a').
Explanation:

The Bellman equation essentially balances exploration and exploitation.
The learning rate (α) determines how much the AI prioritizes the new information (reward) vs. the existing Q-value.
The discount factor (γ) considers the importance of future rewards. A higher γ emphasizes long-term gains.
As the AI plays more games, the Q-table gets populated with better estimates of future rewards for each state-action pair. This allows the AI to make better choices that lead to winning the game.
Additional Notes:

You can represent the empty spaces, player 1 (X), and player 2 (O) with numerical values for the board state and actions.
Techniques like experience replay can be used to improve the learning process by storing past experiences and replaying them for further learning.
By implementing Q-learning with a Tic-Tac-Toe game, you can create an AI that gets progressively better at playing the game as it learns from its experiences.

'''

# -------------------------------------------------------------------------------------------

'''
Este código define una clase QLearningAgent que implementa el algoritmo de Q-learning utilizando TensorFlow. El agente tiene un método start para iniciar un episodio, 
un método step para tomar un paso basado en el estado actual y la recompensa recibida, y un método learn para actualizar la red neuronal basado en la recompensa y el 
próximo estado. El método get_action se utiliza para seleccionar una acción basada en el estado actual y la política de exploración/explotación.
'''
class QLearningAgent:
    def __init__(self, alpha=0.5, discount=0.95, exploration_rate=1.0):
        self.alpha = alpha
        self.discount = discount
        self.exploration_rate = exploration_rate
        self.state = None
        self.action = None

        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(32, input_shape=(9,), activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(9)
        ])

        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=alpha), loss='mse')

    def start(self, state):
        self.state = np.array(state)
        self.action = self.get_action(state)
        return self.action

    def get_action(self, state):
        if np.random.uniform(0, 1) < self.exploration_rate:
            action = np.random.choice(9)
        else:
            q_values = self.model.predict(np.array([state]))
            action = np.argmax(q_values[0])
        return action

    def learn(self, state, action, reward, next_state):
        q_update = reward
        if next_state is not None:
            q_values_next = self.model.predict(np.array([next_state]))
            q_update += self.discount * np.max(q_values_next[0])

        q_values = self.model.predict(np.array([state]))
        q_values[0][action] = q_update

        self.model.fit(np.array([state]), q_values, verbose=0)

        self.exploration_rate *= 0.99

    def step(self, state, reward):
        action = self.get_action(state)
        self.learn(self.state, self.action, reward, state)
        self.state = np.array(state)
        self.action = action
        return action
