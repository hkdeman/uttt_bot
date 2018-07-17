#!/usr/bin/env python3

import sys
from players.toeminator import Toeminator
from players.random import Random

def main():
    line = sys.stdin.readline()
    while line:
        player.process_input(line.strip())
        line = sys.stdin.readline()


if __name__ == "__main__":
    player = Toeminator()
    # player = Random()
    main()