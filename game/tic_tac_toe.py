import numpy as np
from game.board import Board
from game.player import Player

class TicTacToe:
    def __init__(self, player1:Player, player2:Player) -> None:
        self.board = Board()
        self.valid_moves = self.board.valid_moves
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.winner = None
        self.history = []

    def is_winner(self):
        if self.all_horizontals():
            return self.all_horizontals()
        elif self.all_verticals():
            return self.all_verticals()
        elif self.all_diagonals():
            return self.all_diagonals()
        return None
    
    def all_horizontals(self):
        for i in range(self.board.size):
            if np.all(self.board.grid[i] == self.player1.symbol):
                return self.player1.symbol
            elif np.all(self.board.grid[i] == self.player2.symbol):
                return self.player2.symbol
        return None

    def all_verticals(self):
        for i in range(self.board.size):
            if np.all(self.board.grid[:, i] == self.player1.symbol):
                return self.player1.symbol
            elif np.all(self.board.grid[:, i] == self.player2.symbol):
                return self.player2.symbol
        return None
    
    def all_diagonals(self):
        if (np.all(self.board.grid.diagonal() == self.player1.symbol) or 
            np.all(np.fliplr(self.board.grid).diagonal() == self.player1.symbol)):
            return self.player1.symbol
        elif (np.all(self.board.grid.diagonal() == self.player2.symbol) or 
            np.all(np.fliplr(self.board.grid).diagonal() == self.player2.symbol)):
            return self.player2.symbol
        return None
    
    def execute_move(self, player:Player, move):
        self.board.grid[move[0], move[1]] = player.symbol

    def update_valid_moves(self, move):
        self.valid_moves.remove(move)

    def switch_turns(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        elif self.current_player == self.player2:
            self.current_player = self.player1    

    def announce_winner(self):
        if self.player1.symbol == self.winner:
            print(f"{self.player1.name} won.")
        elif self.player2.symbol == self.winner:
            print(f"{self.player2.name} won.")

    def announce_draw(self):
        print("Game was a draw")