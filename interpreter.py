from board import Board

def input_move():
    valid_inputs = {
        'l': 'left',
        'r': 'right',
        'u': 'up',
        'd': 'down',
        'q': 'quit',
        'g': 'go',
    }
    result = input("Enter one of l(eft), r(ight), u(p), d(own), q(uit), g(o): ")
    return valid_inputs.get(result) or result

# COMMANDS = {
#     '?': HelpCmd,
#     'help': HelpCmd,
#     'up': MoveCmd,
#     'down': MoveCmd,
#     'left': MoveCmd,
#     'right': MoveCmd,
#     'go': GoCmd,
#     'quit': QuitCmd,
#     'seed': SeedCmd,
#     'why': WhyCmd,
#     '[]': BoardStateCmd,
#     '[[': SetBoardCmd,
#     'test': TestCmd
# }

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
            command = input_move()
            if command == 'quit':
                break
            elif command == 'go':
                board.go(move)
            elif command.startswith('s'):
                board.reset_board(int(command[1:]))
                board.go()
            else:
                if command != '':
                    move = command
                if move not in moves:
                    print(f"Invalid move: {move}")
                else:
                    print(f"Moving {move}")
                    board.move(move)
                    board.add_tile()
                    board.display()
        board.report()
