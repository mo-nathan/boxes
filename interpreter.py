from board import Board
import sys
import re

# Actions
def board_state(board, move, key, command):
    if command.startswith("[["):
        try:
            if re.fullmatch("[0-9, [\\]]+", command):
                new_state = eval(command)
                if valid_board(new_state):
                    board.board = new_state
                else:
                    print(f"Invalid board state: {command}")
        except Exception as e:
            print(f"Error interpreting '{command}' as a board state.")
            print(e)
    board.display()

def valid_board(board):
    return isinstance(board, list) and len(board) == 4 and valid_rows(board)

def valid_rows(board):
    for row in board:
        if not valid_row(row):
            return False
    return True

def valid_row(row):
    return isinstance(row, list) and len(row) == 4 and valid_elements(row)

def valid_elements(elements):
    for element in elements:
        if not isinstance(element, int):
            return False
    return True

def go(board, move, key, command):
    board.go(move)

def move_board(board, move, key, command):
    if key:
        move = key
    print(f"Moving {move}")
    board.move(move)
    board.add_tile()
    board.display()

def print_help(board, move, key, command):
    print("\nSimply hitting <return> will apply the recommended move.\n")
    print("Interactive commands (these can be abbreviated):")
    print("  left, right, up, down : Move the board in the given direction")
    print("  why : Explain the recommendation")
    print("  go : Do the recommended moves until there are no more moves")
    print("  [] : Print the current board state")
    print("  seed # : Reset the board and set the random seed")
    print("  ?, help : Print this help")
    print("  quit : Quit the program")
    print("\nEnter a board state to reset the board to that state, for example:")
    print("  [[2,0,2,0],[0,2,0,2],[2,0,2,0],[0,2,0,2]]")

def quit_program(board, move, key, command):
    sys.exit()

def seed(board, move, key, command):
    args = command.split(' ')
    if len(args) == 2:
        if args[1].isnumeric():
            board.reset_board(int(args[1]))
            board.go()
            return
    print(f"Unable to find seed in '{command}'")

def why(board, move, key, command):
    board.debugger = True
    board.display()
    board.evaluate(board.can_move())
    board.debugger = False

COMMANDS = {
    'left': move_board,
    'right': move_board,
    'up': move_board,
    'down': move_board,
    'why': why,
    'go': go,
    '[]': board_state,
    '?': print_help,
    'help': print_help,
    'seed': seed,
    'quit': quit_program
}

def input_command():
    command = input("Enter command (? to list commands): ").strip()
    if command:
        cmd = command.split(' ')[0]
        if command.startswith("[["):
            return board_state, None, command
        for key in COMMANDS.keys():
            if key.startswith(cmd):
                return COMMANDS[key], key, command
    else:
        return move_board, None, command
    return None, None, command

class Interpreter:
    def run(self):
        board = Board()
        board.reset_board()
        print(board.seed)
        board.display()

        while True:
            moves = board.can_move()
            move = board.make_recommendation(moves)
            if move == None:
                print("Nothing to recommend")
                board.report()
            action, key, command = input_command()
            if action:
                action(board, move, key, command)
            else:
                print(f"\n*** INVALID COMMAND: {command}\n")
        board.report()
