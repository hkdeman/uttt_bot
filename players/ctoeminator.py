import random

from engine import MainBoardCoords, SubBoardCoords, SubBoard
from players.stdout import StdOutPlayer
from tactics.parser import parse
from tactics.algorithm import C2MCTS
from tactics.helper import moves_mapper, reverse_moves_mapper

class CToeminator(StdOutPlayer):
    def __init__(self):
        super().__init__()
        
    def get_my_move(self):  # -> Tuple[MainBoardCoords, SubBoardCoords]
        new_board = parse(self.main_board)
        last_turn = self.main_board.sub_board_next_player_must_play
        mcts = C2MCTS(board=new_board,last_turn=reverse_moves_mapper[(last_turn.row,last_turn.col)] if last_turn is not None else None)
        sub_board, pos = mcts.run()
        # print("----------------")
        # print(sub_board)
        # print(pos)
        # print("----------------")        
        return moves_mapper[sub_board], moves_mapper[pos]