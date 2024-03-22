import numpy as np
from game.positions import Positions

class Board:
    def __init__(self, size = 3):
        self.size = size
        self.grid = np.full((size, size), 0)
        self.positions = Positions()
        self.valid_moves = list(self.positions.__dict__.values())        

    def display(self):
        print(self.grid)

    def is_full(self):
        return not np.any(self.grid == 0)
    
    def get_board_state(self):
        return self.grid