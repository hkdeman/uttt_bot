import numpy as np
from tactics.helper import Turns, WIN_POSES

class TicTacToe:
    def __init__(self, grid):
        self.grid = grid
        self.winner = None
    
    def get_grid(self): return list(self.grid)
    
    def get_winner(self): return self.winner
    
    def get_positions(self,player): return list(np.where(self.grid==player)[0])

    def get_free_moves(self): return np.where(self.grid==Turns.Empty.value)[0] if not self.did_someone_win() else []

    def move(self, turn, pos):
        if self.grid[pos] == Turns.Empty.value and not self.is_game_done():
            self.grid[pos] = turn
            return True
        else:
            return False
        
    def did_win(self,player):
        player=set(player)
        for pos in WIN_POSES:
            if pos.issubset(player):
                return True
        return False
    
    def is_board_full(self):
        return len(self.get_free_moves())==0

    def did_someone_win(self):
        x_pos = self.get_positions(Turns.X.value)
        o_pos = self.get_positions(Turns.O.value)
        
        x_win, o_win = self.did_win(x_pos), self.did_win(o_pos)
        if x_win or o_win: return True
        return False

    def is_game_done(self):
        x_pos = self.get_positions(Turns.X.value)
        o_pos = self.get_positions(Turns.O.value)
        
        x_win, o_win = self.did_win(x_pos), self.did_win(o_pos)
        if x_win:
            self.winner = Turns.X.value
            return True
        elif o_win:
            self.winner = Turns.O.value
            return True
        elif self.is_board_full():
            return True
        return False