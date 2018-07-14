from node import Node

class Tree:
    def __init__(self, turn):
        self._root = Node(turn)
    
    def set_root(self, node):
        self._root = node
    
    def get_root(self):
        return self._root