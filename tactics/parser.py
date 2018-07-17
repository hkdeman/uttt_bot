import numpy as np
import time

def parse(board):
    grid = []
    for sub_boards in board:
        for sub_board in sub_boards:
            sub_grid = []
            for row in sub_board:
                for cell in row:
                    sub_grid.append(int(str(cell)))
            grid.append(np.array(sub_grid))
    grid = np.array(grid)
    return grid