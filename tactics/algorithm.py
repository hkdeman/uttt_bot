from tactics.helper import GameState, Turns, switch_turns, current_milli_time
from random import choice
from tactics.uttt import UltimateTicTacToe
from copy import deepcopy as clone
from tactics.tree import Tree
import numpy as np
from tactics.nn import NeuralNetwork
from multiprocessing import Pool, Process, Manager
import operator
from threading import Thread

possible_moves = []
class MCTSRunner:
    def __init__(self, board, last_turn, turn=Turns.X.value, timeout=20, before=1):
        self._cloned_board = clone(UltimateTicTacToe(board=board, last_turn=last_turn))
        self._moves = self._cloned_board.get_free_moves()
        games = []
        for move in self._moves:
            _cloned_board = clone(self._cloned_board)
            board = _cloned_board.move(turn,*move)
            if board:
                board_list = _cloned_board.get_board_list()
                games.append((board_list,last_turn,turn,timeout,before, move))
        self.games = games
    
    def trun(self):
        threads = []
        manager = Manager()
        return_dict = manager.dict()
        for game in self.games:
            t = Thread(target=self.initiate_algorithm, args=(game,return_dict))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()

        chosen_move = max(return_dict.copy(), key=operator.itemgetter(1))
        return chosen_move

    def run(self):
        processes = []
        manager = Manager()
        return_dict = manager.dict()
        for game in self.games:
            p = Process(target=self.initiate_algorithm, args=(game,return_dict))
            p.start()
            processes.append(p)
        for proc in processes:
            proc.join()

        best_moves = return_dict.copy()
        max_val = best_moves[self._moves[0]]
        bmind = self._moves[0]
        for key in best_moves:
            if best_moves[key] > max_val:
                max_val = best_moves[key]
                bmind = key
        
        return bmind

    def initiate_algorithm(self, args, return_dict):
        mcts = clone(MPMCTS(*args))
        val = mcts.run()
        return_dict[val[1]] = val[0]
        
class MPMCTS:
    def __init__(self, board, last_turn,turn, timeout, before, move):
        self.turn = turn
        self.board = board
        self._cloned_board = None
        self.mct = None
        self.timeout = timeout
        self.before = before
        self.last_turn = last_turn
        self.move = move
    
    def run(self):
        if self.mct == None:
            # if new tree then initialize that it came from the opposite player
            self.mct = clone(Tree(switch_turns(self.turn)))
        else:
            # if the tree exists look for the node if it contains that
            children =self.mct.get_root().get_children()
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
                    self.mct = clone(Tree(switch_turns(self.turn)))
            else:
                # otherwise initialize new tree
                self.mct = clone(Tree(switch_turns(self.turn)))
        
        start_time = current_milli_time()
        while current_milli_time() - start_time < self.timeout - self.before:
            self._cloned_board = clone(UltimateTicTacToe(board=self.board, last_turn=self.last_turn))
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
            node = node.add_child(next_move)
            self.play_cloned_board(move=next_move, turn=node.get_turn())
             
        # to give more precendence to the bigger board
        # to make sure long term goals are in mind

        if (won and self._cloned_board.get_winner() == GameState.WIN):
            node.small_board_won()
            # next_move = node.get_move()
        # elif (len(self._cloned_board.get_free_moves())<3):
        #     node.set_as_desirable(-0.3)
        
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
            self.backpropogate(GameState.LOSE if node.get_turn()==current_simulation_turn else GameState.WIN, node)

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
        return self._cloned_board.move(turn,*move)
    
    def choose_best_next_move(self):
        # move = sorted(self.mct.get_root().get_children(), key=lambda n: n.get_score())[-1]
        # self.mct.set_root(move)

        next_move = (self.mct.get_root().get_score(),self.move)
        return next_move

class C2MCTS:
    def __init__(self, board, last_turn,turn=Turns.X.value, timeout=50, before=1):
        self.turn = turn
        self.board = board
        self._cloned_board = None
        self.mct = None
        self.timeout = timeout
        self.before = before
        self.last_turn = last_turn
        self.nn = NeuralNetwork()
        self.nn.load("2018-07-19 22:29:06")
    
    def run(self):
        if self.mct == None:
            # if new tree then initialize that it came from the opposite player
            self.mct = Tree(switch_turns(self.turn))
        else:
            # if the tree exists look for the node if it contains that
            children =self.mct.get_root().get_children()
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
            self._cloned_board = clone(UltimateTicTacToe(board=self.board, last_turn=self.last_turn))
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
            node = node.add_child(next_move)
            self.play_cloned_board(move=next_move, turn=node.get_turn())
        # to give more precendence to the bigger board
        # to make sure long term goals are in mind

        # if (won and self._cloned_board.get_winner() == GameState.WIN):
        #     node.small_board_won()
        #     next_move = node.get_move()
        # elif (len(self._cloned_board.get_free_moves())<3):
        #     node.set_as_desirable(-0.5)
        
        return node

    def roll_out(self, node):
        # second approach, use neural net to predict
        old_board = self._cloned_board.get_board_list()
        if not self._cloned_board.is_game_done():
            move = choice(self._cloned_board.get_free_moves())
            new_board = clone(old_board)
            new_board[move[0]][move[1]] = 1
            feature = np.concatenate((old_board.flatten(),new_board.flatten()),axis=0).reshape((18,9,1))
            score = self.nn.predict(np.array([feature]))[0]
            if score[0]>0.5:
                self.backpropogate(GameState.WIN, node)        
            elif score[1]>0.5:
                self.backpropogate(GameState.LOSE, node)            
            else:
                self.backpropogate(GameState.DRAW, node)
        else:
            if self._cloned_board.get_winner() == None:
                self.backpropogate(GameState.DRAW, node)
            else:
                self.backpropogate(GameState.WIN if node.get_turn()==Turns.X.value else GameState.LOSE, node)
    
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
        move = sorted(self.mct.get_root().get_children(), key=lambda n: n.get_score())[-1]
        # self.mct.set_root(move)
        return move.get_move()

class MCTS:
    def __init__(self, board, last_turn,turn=Turns.X.value, timeout=200, before=1):
        self.turn = turn
        self.board = board
        self._cloned_board = None
        self.mct = None
        self.timeout = timeout
        self.before = before
        self.last_turn = last_turn
    
    def run(self):
        if self.mct == None:
            # if new tree then initialize that it came from the opposite player
            self.mct = Tree(switch_turns(self.turn))
        else:
            # if the tree exists look for the node if it contains that
            children =self.mct.get_root().get_children()
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
            self._cloned_board = clone(UltimateTicTacToe(board=self.board, last_turn=self.last_turn))
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
            node = node.add_child(next_move)
            self.play_cloned_board(move=next_move, turn=node.get_turn())
        # to give more precendence to the bigger board
        # to make sure long term goals are in mind

        # if (won and self._cloned_board.get_winner() == GameState.WIN):
        #     node.small_board_won()
        #     next_move = node.get_move()
        # elif (len(self._cloned_board.get_free_moves())<3):
        #     node.set_as_desirable(-0.5)
        
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
            self.backpropogate(GameState.LOSE if node.get_turn()==current_simulation_turn else GameState.WIN, node)

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
        move = sorted(self.mct.get_root().get_children(), key=lambda n: n.get_score())[-1]
        # self.mct.set_root(move)
        return move.get_move()

