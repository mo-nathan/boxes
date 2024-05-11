from board import Board

def tests():
    test_board([[64, 32, 2, 0], [16, 0, 0, 0], [8, 0, 0, 0], [0, 4, 0, 0]], "left")
    test_board([[64, 2, 8, 0], [16, 32, 2, 0], [8, 4, 0, 0], [2, 4, 4, 0]], "up")
    test_board([[64, 8, 8, 0], [16, 2, 8, 16], [8, 32, 2, 4], [2, 16, 2, 2]], "down")
    test_board([[2, 0, 0, 0], [8, 2, 0, 0], [16, 8, 8, 4], [64, 16, 2, 4]], "left")
    test_board([[8, 4, 4, 0], [4, 0, 0, 0], [0, 0, 0, 4], [0, 0, 0, 0]], "right")
    
def test_board(initial_state, pref):
    result = run_board(initial_state, pref)
    if result != pref:
        print(f"\n\n**** FAILURE ****: Expected {pref} got {result}")
        run_board(initial_state, pref, True)
        print("\n\n")
    else:
        print("success")

def run_board(initial_state, pref, debug = False):
    board = Board()
    board.board = initial_state
    board.debugger = debug
    if debug:
        board.display()
    scores = board.evaluate(board.can_move())
    if debug:
        print(f"Scores: {scores}")
    return max(scores)[1]
