#!/usr/bin/env python3

import sys
from players.toeminator import Toeminator
from players.ctoeminator import CToeminator
from players.random import Random
from players.nsquare import NSquare, NMCTS
from players.cnsquare import CNSquare

def main():
    line = sys.stdin.readline()
    while line:
        player.process_input(line.strip())
        line = sys.stdin.readline()


if __name__ == "__main__":
    # player = Toeminator()
    # player = Random()
    # player = CNSquare()
    player = NMCTS()
    # player = NSquare()
    # player = CToeminator()
    main()