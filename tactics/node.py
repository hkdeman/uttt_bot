from tactics.helper import switch_turns, GameState
from math import sqrt, log

UCB_CONSTANT = 5

class Node:
    def __init__(self, parent, turn, move):
        self._move = move
        self._parent = parent
        self._children = []
        self._turn = turn
        self._wins = 0
        self._visits = 0
        self._is_game_over = False
        self._is_desirable = False

    def get_move(self): return self._move
    
    def get_parent(self): return self._parent
    
    def get_turn(self): return self._turn
    
    def is_game_over(self): return self._is_game_over
    
    def get_children(self): return self._children    

    def get_wins(self): return self._wins

    def get_visits(self): return self._visits

    def get_ucb_value(self):
        return (self._wins/self._visits) + sqrt(UCB_CONSTANT*log(self.get_parent().get_visits()/self._visits))

    def set_game_as_over(self):
        self._is_game_over = True
        self.set_as_desirable(1)
    
    def add_child(self, move):
        child = Node(move=move, parent=self, turn=switch_turns(self._turn))
        self._children.append(child)
        return child
    
    def small_board_won(self):
        self.set_as_desirable(0.5)
        self.get_parent().set_as_desirable(-1)

    def set_as_desirable(self, value):
        if(not self._is_desirable):
            self._wins += value*100000000
            self._is_desirable = True
        self._visits = 1

    def update_stats(self, game_state):
        if game_state == GameState.WIN:
            self._wins+=1
        elif game_state == GameState.LOSE:
            self._wins-=1
        else:
            self._wins+=0.5
        
        self._visits+=1

    def get_score(self):
        return self._wins/self._visits

    def __str__(self):
        return str(self._move)