from helper import GameState, Turns, switch_turns, current_milli_time
from random import choice
from uttt import UltimateTicTacToe
from copy import deepcopy as clone
from tree import Tree
import numpy as np

class MCTS:
    def __init__(self, turn, board, timeout=500, before=1):
        self.turn = turn
        self.board = board
        self._cloned_board = None
        self.mct = None
        self.timeout = timeout
        self.before = before
    
    def run(self):
        if self.mct == None:
            # if new tree then initialize that it came from the opposite player
            self.mct = Tree(switch_turns(self.turn))
        else:
            # if the tree exists look for the node if it contains that
            children =self.mct.get_root().get_children
            if len(children) !=0:
                contained = False
                node = children[0]
                for n in children:
                    if n.get_move() == self._cloned_board.get_previous_move():
                        contained = True
                        node = n
                if contained:
                    self.mct.set_root(node)
                else:
                    # otherwise initialize new tree
                    self.mct = Tree(switch_turns(self.turn))
            else:
                # otherwise initialize new tree
                self.mct = Tree(switch_turns(self.turn))

        start_time = current_milli_time()
        while current_milli_time() - start_time < self.timeout - self.before:
            self._cloned_board = clone(UltimateTicTacToe(self.board))
            self.roll_out(self.expansion(self.selection(self.mct.get_root())))
        return self.choose_best_next_move()

    def selection(self, node):
        while(len(self._cloned_board.get_free_moves())==len(node.get_children()) and len(node.get_children())!=0):
            node = self.select_ucb_child(node.get_children())
            self.play_cloned_board(node.get_move(), node.get_turn())
        return node
    
    def expansion(self, node):
        next_move = None
        won = self._cloned_board.is_game_done()
        if (won):
            node.set_game_as_over()
        else:
            # if tree contains the node
            for move in self._cloned_board.get_free_moves():
                contained = False
                for child in node.get_children():
                    if child.get_move() == move:
                        contained = True
                
                if not contained:
                    next_move = move
                    break
        node.add_child(next_move)
        # self.play_cloned_board(node.get_move(), node.get_turn())
        # to give more precendence to the bigger board
        # to make sure long term goals are in mind

        # won = False # appropriately update this later
        # if (won == GameState.WIN):
        #     node.small_board_won()
        #     next_move = node.get_move()
        # elif (self._cloned_board.get_at_pos() == Turns.Empty.value):
        #     node.set_as_desirable(-0.2)
        
        return node

    def roll_out(self, node):
        # first approach, random sample to see
        current_simulation_turn = switch_turns(node.get_turn()) 
        while not self._cloned_board.is_game_done():
            moves = self._cloned_board.get_free_moves()
            move = choice(moves)
            self.play_cloned_board(move, current_simulation_turn)
            current_simulation_turn = switch_turns(current_simulation_turn)
        
        if self._cloned_board.get_winner() == None:
            self.backpropogate(GameState.DRAW, node)
        else:
            self.backpropogate(GameState.WIN if node.get_turn()==current_simulation_turn else GameState.LOSE, node)

        # second approach, use neural net to predict
    
    def backpropogate(self, game_state, node):
        index = 0 # to alternate between wins and loses
        while True:
            if game_state == GameState.DRAW:
                node.update_stats(game_state)
            elif index % 2 == 0:
                node.update_stats(game_state)
            else:
                node.update_stats(GameState.LOSE if game_state == GameState.WIN else GameState.WIN)
            
            node = node.get_parent()
            index+=1

            if node == None:
                break

    def select_ucb_child(self, nodes):
        return sorted(nodes,key=lambda n:n.get_ucb_value())[-1]

    def play_cloned_board(self, move, turn):
        self._cloned_board.move(turn,*move)
    
    def choose_best_next_move(self):
        l = self.mct.get_root().get_children()
        move = sorted(self.mct.get_root().get_children(), key=lambda n: n.get_score())
        move= move[-1]
        self.mct.set_root(move)
        return move.get_move()


grid = np.array([np.zeros(9) for _ in range(9)])
mcts = MCTS(Turns.X.value,grid)
print(mcts.run())