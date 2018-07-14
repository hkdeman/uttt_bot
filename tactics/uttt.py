from ttt import TicTacToe
from helper import Turns, WIN_POSES
import numpy as np 

class UltimateTicTacToe:
    def __init__(self, board):
        self.board = [TicTacToe(grid) for grid in board]
        self.winner = None
        self.last_turn = None

    def get_last_turn(self): return self.last_turn
    
    def get_board(self): return self.board

    def get_winner(self): return self.winner

    def get_board_list(self): return np.array([grid.get_grid() for grid in self.board])
    
    def get_grid_to_move(self): return self.last_turn
    
    def get_sub_board(self, board_pos): return self.grid[board_pos]
    
    def get_free_moves(self): 
        free_moves = []
        for i, sub_board in enumerate(self.board):
            free_moves.extend([(i,move) for move in sub_board.get_free_moves()])
        return free_moves

    def get_positions(self, player):
        positions = []
        for i, sub_board in enumerate(self.board):
            if sub_board.is_game_done() and sub_board.get_winner()==player:
                positions.append(i)
        return positions

    def move(self,turn, grid, pos):
        if self.last_turn == None:
            if self.board[grid].move(turn, pos):
                self.last_turn = grid
                return True
            return False
        elif grid == self.last_turn:
            if self.board[grid].move(turn, pos):
                self.last_turn = grid
                return True
            return False
        return False
    
    def did_win(self, player):
        player=bytearray(player)
        for pos in WIN_POSES:
            if pos in player:
                return True
        return False
    
    def is_game_done(self):
        x_pos = self.get_positions(Turns.X.value)
        o_pos = self.get_positions(Turns.O.value)

        x_win, o_win = self.did_win(x_win), self.did_win(o_pos)

        if x_win or o_win:
            self.winner = Turns.X.value if x_win else Turns.O.value
            return True
        return False