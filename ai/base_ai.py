import random
from game.player import Player

class BaseAI(Player):
    def __init__(self, name:str, symbol:int): 
        super().__init__(name, symbol)

    def select_move(self, **kwargs):
        valid_moves = kwargs["valid_moves"]
        return random.choice(valid_moves)
    
