import random

from engine import MainBoardCoords, SubBoardCoords, SubBoard
from players.stdout import StdOutPlayer
from tactics.parser import parse
from tactics.helper import moves_mapper, reverse_moves_mapper
from tactics.nn import NeuralNetwork
from copy import deepcopy
import numpy as np
 
class CNSquare(StdOutPlayer):
    def __init__(self):
        super().__init__()
        self.nn = NeuralNetwork()
        self.nn.load("2018-07-19 22:29:06")
        
    def get_my_move(self):  # -> Tuple[MainBoardCoords, SubBoardCoords]
        current_board = parse(self.main_board)
        last_turn = self.main_board.sub_board_next_player_must_play
        features = [] # so you can map 
        all_moves = [] # these two by indexes
        if last_turn is None:
            moves = self.main_board.get_playable_coords()
            for move in moves:
                sub_board_parsed = reverse_moves_mapper[(move.row,move.col)]
                sub_moves = self.main_board.get_sub_board(move).get_playable_coords()                                    
                for sub_move in sub_moves:
                    next_board = deepcopy(current_board)
                    sub_move_parsed = reverse_moves_mapper[(sub_move.row,sub_move.col)]
                    next_board[sub_board_parsed][sub_move_parsed] = 1
                    new_board = np.concatenate((current_board.flatten(),next_board.flatten()),axis=0)
                    features.append(new_board.reshape((9,9,2)))
                    all_moves.append((move,sub_move))
        else:
            sub_moves = self.main_board.get_sub_board(last_turn).get_playable_coords()
            sub_board_parsed = reverse_moves_mapper[(last_turn.row,last_turn.col)]
            for sub_move in sub_moves:
                sub_move_parsed = reverse_moves_mapper[(sub_move.row,sub_move.col)]                
                next_board = deepcopy(current_board)
                next_board[sub_board_parsed][sub_move_parsed] = 1
                new_board = np.concatenate((current_board.flatten(),next_board.flatten()),axis=0)
                features.append(new_board.reshape((9,9,2)))
                all_moves.append((last_turn,sub_move))
        features = np.array(features)
        scores = self.nn.predict(features)
        # print(scores)
        max_score_index = 0
        max_score = -1 # gonna lose completely
        least_o_score = -1
        least_o_index = 0
        for i, score in enumerate(scores):
            if score[0] > max_score:
                max_score = score[0]
                max_score_index = i
            if score[1] > least_o_score:
                least_o_score = score[1]
                least_o_index = i
        
        if max_score < 0:
            move = all_moves[least_o_index]
            return move[0],move[1]
        else:
            move = all_moves[max_score_index]
            return move[0],move[1]