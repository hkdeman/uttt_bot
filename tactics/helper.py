from enum import Enum
import time

class Turns(Enum):
    X = 1
    O = 2
    Empty = 0

class GameState(Enum):
    WIN = 1
    LOSE = -1
    DRAW = 0.5
    NOT_DONE = 0 


def switch_turns(turn):
    if turn == Turns.X.value:
        return Turns.O.value
    elif turn == Turns.O.value:
        return Turns.X.value
    else:
        return Turns.Empty.value

current_milli_time = lambda: int(round(time.time() * 1000))

winner_positions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
WIN_POSES = [set(pos) for pos in winner_positions]

class Move:
    def __init__(self,row,col):
        self.row = row
        self.col = col

moves_mapper = {
    0:Move(0,0),
    1:Move(0,1),
    2:Move(0,2),
    3:Move(1,0),
    4:Move(1,1),
    5:Move(1,2),
    6:Move(2,0),
    7:Move(2,1),
    8:Move(2,2),
}

reverse_moves_mapper = {
    (0,0):0,
    (0,1):1,
    (0,2):2,
    (1,0):3,
    (1,1):4,
    (1,2):5,
    (2,0):6,
    (2,1):7,
    (2,2):8,
}