from ttt import TicTacToe
from helper import Turns, WIN_POSES
import numpy as np 

class UltimateTicTacToe:
    def __init__(self, board, last_turn):
        self.board = [TicTacToe(grid) for grid in board]
        self.winner = None # None as nobody won
        self.last_turn = last_turn # None because nobody played before
        self.previous_move = None # None on the start of the game

    def get_last_turn(self): return self.last_turn
    
    def get_previous_move(self): return self.previous_move

    def get_board(self): return self.board

    def get_winner(self): return self.winner

    def get_board_list(self): return np.array([grid.get_grid() for grid in self.board])
    
    def get_grid_to_move(self): return self.last_turn
    
    def get_sub_board(self, board_pos): return self.board[board_pos]
    
    def is_board_full(self):
        for sub_board in self.board:
            if not sub_board.is_game_done():
                return False
        return True

    def get_free_moves(self): 
        free_moves = []
        if self.last_turn == None:
            for i, sub_board in enumerate(self.board):
                free_moves.extend([(i,move) for move in sub_board.get_free_moves()])
        else:
            if self.board[self.last_turn].is_game_done():
                for i, sub_board in enumerate(self.board):
                    free_moves.extend([(i,move) for move in sub_board.get_free_moves()])
            else:
                free_moves.extend([(self.last_turn, move) for move in self.board[self.last_turn].get_free_moves()])
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
                self.last_turn = grid if not self.board[grid].is_game_done() else None                
                self.previous_move = (grid,pos)
                return True
            return False
        elif grid == self.last_turn:
            if self.board[grid].move(turn, pos):
                self.last_turn = grid if not self.board[grid].is_game_done() else None
                self.previous_move = (grid,pos)
                return True
            return False
        return False
    
    def did_win(self, player):
        player=set(player)
        for pos in WIN_POSES:
            if pos.issubset(player):
                return True
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

# board = np.array([
#     np.array([1,1,1,0,0,0,0,0,0]),
#     np.array([0,0,0,0,0,0,0,0,0]),
#     np.array([0,0,0,0,0,0,0,0,0]),
#     np.array([0,0,0,0,0,0,0,0,0]),
#     np.array([0,0,0,0,0,0,0,0,0]),
#     np.array([0,0,0,0,0,0,0,0,0]),
#     np.array([0,0,0,0,0,0,0,0,0]),
#     np.array([0,0,0,0,0,0,0,0,0]),
#     np.array([0,0,0,0,0,0,0,0,0]),    
# ])
# uttt = UltimateTicTacToe(board,last_turn=0)
# print(uttt.get_free_moves())