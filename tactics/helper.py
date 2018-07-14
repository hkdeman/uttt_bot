from enum import Enum
import time

class Turns(Enum):
    X = 1
    O = -1
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

winner_positions = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,5),(2,5,8),(0,4,8),(2,4,6)]
WIN_POSES = [bytearray(pos) for pos in winner_positions]