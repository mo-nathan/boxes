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

# Current median moves of 3 averages of 1000 runs: 1518.81
# Previous median moves of 3 averages of 1000 runs: 855.347
# Previous median moves of 3 averages of 1000 runs: 554.132
# Previous median moves of 3 averages of 1000 runs: 540.996

# Sun May 12 10:06:23 EDT 2024

# Average moves: 1619.48
# Average sum: 3788.64
# Max tile distribution:
# 	512: 2
# 	1024: 16
# 	2048: 65
# 	4096: 17
# Max board: [[4096, 64, 8, 2], [2048, 128, 16, 4], [1024, 64, 32, 2], [512, 32, 16, 8]]
# Best seed: 6461335521806861828
# Worst seed: 5562406088144523058
# Sun May 12 10:18:34 EDT 2024
# Average moves: 1431.33
# Average sum: 3342.26
# Max tile distribution:
# 	256: 2
# 	512: 3
# 	1024: 31
# 	2048: 51
# 	4096: 13
# Max board: [[4096, 128, 16, 2], [2048, 256, 64, 4], [1024, 128, 16, 8], [256, 64, 4, 2]]
# Best seed: 8325191424033022356
# Worst seed: 3775241873814919289
# Sun May 12 10:29:31 EDT 2024
# Average moves: 1518.81
# Average sum: 3545.46
# Max tile distribution:
# 	256: 2
# 	512: 5
# 	1024: 19
# 	2048: 55
# 	4096: 19
# Max board: [[4096, 64, 8, 2], [2048, 128, 16, 4], [512, 256, 32, 2], [64, 16, 64, 4]]
# Best seed: 4407157200292233652
# Worst seed: 5159205778343274897
# Sun May 12 10:41:03 EDT 2024
