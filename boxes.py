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

# Current median moves of 3 averages of 1000 runs: 855.347
# Previous median moves of 3 averages of 1000 runs: 554.132
# Previous median moves of 3 averages of 1000 runs: 540.996

# Sat May 11 11:09:19 EDT 2024
# Average moves: 855.347
# Average sum: 2001.222
# Max tile distribution:
# 	128: 8
# 	256: 61
# 	512: 146
# 	1024: 565
# 	2048: 220
# Max board: [[4, 16, 32, 2048], [2, 32, 256, 1024], [4, 16, 128, 512], [8, 4, 16, 256]]
# Best seed: 4224044503291101573
# Worst seed: 2542187498084904923
# Sat May 11 11:10:40 EDT 2024
# Average moves: 835.239
# Average sum: 1952.966
# Max tile distribution:
# 	64: 1
# 	128: 16
# 	256: 54
# 	512: 177
# 	1024: 540
# 	2048: 212
# Max board: [[2, 4, 8, 2], [8, 16, 32, 8], [16, 64, 128, 64], [2048, 1024, 512, 256]]
# Best seed: 5682547505023034735
# Worst seed: 7172620897910841814
# Sat May 11 11:12:00 EDT 2024
# Average moves: 837.738
# Average sum: 1959.254
# Max tile distribution:
# 	64: 1
# 	128: 17
# 	256: 55
# 	512: 170
# 	1024: 548
# 	2048: 209
# Max board: [[2048, 32, 8, 4], [1024, 256, 64, 8], [512, 128, 32, 4], [32, 16, 8, 2]]
# Best seed: 551776581505276437
# Worst seed: 8080923224547169001
# Sat May 11 11:13:20 EDT 2024
