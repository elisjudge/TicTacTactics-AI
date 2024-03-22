from game.player import Player
import numpy as np
import random

class TrainedAI(Player):
    def __init__(self, name:str, symbol:int, generation:int, learning_rate=0.1, discount_factor=0.9, epsilon=0.1): 
        super().__init__(name, symbol)
        self.generation = generation
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = {}  
        self.exploration_count = 0
        self.total_moves_made = 0

    def select_move(self, **kwargs):
        state = kwargs['state']
        valid_moves = kwargs['valid_moves']
        hashed_state = self.hash_state(state=state)  
        self.total_moves_made += 1

        if np.random.rand() < self.epsilon:
            self.exploration_count += 1
            return random.choice(valid_moves)
        else:
            if hashed_state in self.q_table:  
                q_values = self.q_table[hashed_state] 
                max_q_action = max(q_values, key=q_values.get)
                return eval(max_q_action)  
            else:
                return random.choice(valid_moves)

    def hash_state(self, state):
        return ''.join(str(cell) for row in state for cell in row)

    def update_q_value(self, hashed_state, action, reward, hashed_final_state):
        if hashed_state not in self.q_table:
            self.q_table[hashed_state] = {}
        if hashed_final_state not in self.q_table:
            self.q_table[hashed_final_state] = {}

        old_q = self.q_table[hashed_state].get(str(action), 0)
        max_next_q = max(self.q_table[hashed_final_state].values(), default=0)
        current_q = self.q_table[hashed_state].get(str(action), 0) 
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[hashed_state][str(action)] = new_q  
        return abs(new_q - old_q)