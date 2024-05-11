#!/usr/bin/env python3

import sys
from board import Board
from interpreter import Interpreter
from tests import tests

def command_line_help():
    print("Welcome to Boxes\n")
    print(f"By default just running {sys.argv[0]} will enter interactive mode.\n")
    print(f"{sys.argv[0]} # - Run # games to completion and present a summary.")
    print(f"{sys.argv[0]} test - Run the existing tests.")
    print("\nAnything else will print this message.")

if len(sys.argv) == 1:
    Interpreter().run()
elif sys.argv[1].isnumeric():
    Board().run(int(sys.argv[1]))
elif sys.argv[1][0] == 't':
    tests()
else:
    command_line_help()

# Current median of 3 averages of 1000 runs: 554.132
# Previous median of 3 averages of 1000 runs: 540.996

# Fri May 10 15:07:52 EDT 2024
# Average moves: 554.132
# Average sum: 1668.64
# Max tile distribution:
# 	64: 5
# 	128: 27
# 	256: 97
# 	512: 257
# 	1024: 465
# 	2048: 147
# 	4096: 2
# Max board: [[4, 32, 2, 8], [2, 16, 32, 16], [4, 8, 16, 1024], [2, 4, 32, 4096]]
# Worst seed: 8881331921317771165
# Fri May 10 15:08:46 EDT 2024
# Average moves: 550.691
# Average sum: 1658.456
# Max tile distribution:
# 	64: 1
# 	128: 28
# 	256: 106
# 	512: 250
# 	1024: 468
# 	2048: 145
# 	4096: 2
# Max board: [[2, 4, 8, 2], [8, 32, 16, 4], [16, 128, 32, 16], [2, 8, 64, 4096]]
# Worst seed: 8038581172653389272
# Fri May 10 15:09:39 EDT 2024
# Average moves: 563.143
# Average sum: 1694.878
# Max tile distribution:
# 	64: 2
# 	128: 24
# 	256: 121
# 	512: 232
# 	1024: 466
# 	2048: 155
# Max board: [[2, 8, 64, 2048], [8, 64, 128, 1024], [2, 16, 256, 512], [4, 8, 64, 128]]
# Worst seed: 4179031754838149516
# Fri May 10 15:10:34 EDT 2024
