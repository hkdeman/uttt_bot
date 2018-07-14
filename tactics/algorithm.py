from helper import GameState, Turns, switch_turns, current_milli_time
from random import choice
from uttt import UltimateTicTacToe

class MCTS:
    def __init__(self, turn, board, timeout=500, before=1):
        self._turn = turn
        self._cloned_board = UltimateTicTacToe(board)

    def run(self):
        start_time = current_milli_time()
        while current_milli_time() - start_time < self.timeout - self.before:
            pass

    def selection(self, node):
        while(len(self._cloned_board.get_free_moves())==len(node.get_children()) and len(node.get_children())!=0):
            node = self.select_ucb_child(node.get_children())
            self.play_cloned_board(node.get_move(), node.get_turn())
        return node
    
    def expansion(self, node):
        next_move = None
        won = Board.check_win(self._cloned_board, node.get_turn())
        if (won):
            node.set_game_over()
        else:
            # if tree contains the node
            for move in self._cloned_board.get_free_moves():
                contained = False
                for child in node.get_children():
                    if child.get_move() is move:
                        contained = True
                
                if not contained:
                    next_move = move
                    break

        # to give more precendence to the bigger board
        # to make sure long term goals are in mind

        won = False # appropriately update this later
        if (won == GameState.WIN):
            node.small_board_won()
        move_grid, move_pos = node.get_move()
        elif (self._cloned_board.get_at_pos() == Turns.Empty.value):
            node.set_as_desirable(-0.2)
        
        return node

    def roll_out(self, node):
        # first approach, random sample to see
        won = Board.check_win(self._cloned_board, node.get_turn())
        current_simulation_move = switch_turns(node.get_turn()) 
        while not won:
            move = choice(self._cloned_board.get_free_moves())
            self.play_cloned_board(move,turn)
            current_simulation_move = switch_turns(current_simulation_move)
        
        if self._cloned_board.get_game_state() == GameState.DRAW:
            self.backpropogate(GameState.DRAW, node)
        else:
            self.backpropogate(GameState.WIN if node.get_turn() else GameState.LOSE, node)

        # second approach, use neural net to predict
    
    def backpropogate(self, game_state, node):
        index = 0 # to alternate between wins and loses
        while True:
            if game_state == GameState.DRAW:
                node.update_stats(game_state)
            elif i % 2 == 0:
                node.update_stats(game_state)
            else:
                node.update_stats(GameState.LOSE if game_state == GameState.WIN : GameState.WIN)
            
            node = node.get_parent()
            i+=1

            if node == None:
                break

    # def select_best_ucb_child()
    
    