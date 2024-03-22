from game.board import Board

class Player:
    def __init__(self, name:str, symbol:int): 
        self.name = name
        self.symbol = symbol

    def select_move(self, **kwargs):
        pass
    