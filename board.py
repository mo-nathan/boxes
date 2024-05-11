from random import randrange
from random import seed
from copy import deepcopy
import sys

class Board:
    debugger = False

    def reset_board(self, random_seed = None):
        if random_seed:
            self.seed = random_seed
        else:
            self.seed = randrange(sys.maxsize)
        seed(self.seed)
        self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.move_count = 0
        self.add_tile()
        self.add_tile()

    def display(self):
        print("_"*29)
        for row in self.board:
            print("| {0:4} | {1:4} | {2:4} | {3:4} |".format(
                no_zero(row[0]), no_zero(row[1]), no_zero(row[2]), no_zero(row[3])))
        print("-"*29)
        print(self.board)

    def report(self):
        print(f"Total moves: {self.move_count}")
        print(f"Sum: {sum(flatten(self.board))}")

    def add_tile(self):
        # Insert a 2 or a 4 tile in one of the existing 0 tiles.
        # A 0 title is picked at random and there is an equal
        # probability that a 2 or 4 gets inserted.  The original
        # game seems to be biased towards adding 2s, but I don't
        # know how important that is.
        zeros = self.count_zeros()
        if zeros > 0:
            target = randrange(zeros)
            self.replace_zero(target, randrange(2) * 2 + 2)

    def count_zeros(self):
        count = 0
        for row in self.board:
            for cell in row:
                if cell == 0:
                    count += 1
        return count

    def replace_zero(self, index, value):
        count = 0
        for row in self.board:
            element = 0
            for cell in row:
                if cell == 0:
                    if count == index:
                        row[element] = value
                        return
                    count += 1
                element += 1

    def move(self, direction):
        # Update the board by moving "left", "right", "up", or "down".
        # Extract each vector in the expected direction, calculate the
        # change in that vector, update the vector in the board with
        # the new vector.
        points = 0
        self.move_count += 1
        for index in range(4):
            row = self.vector(direction, index)
            points += row_points(row)
            self.update_vector(direction, index, next_row(row))
        return points

    def vector(self, direction, index):
        result = []
        for i in range(4):
            result.append(self.element(direction, index, i))
        return result

    def element(self, direction, v_index, e_index):
        if direction == "left":
            return self.board[v_index][e_index]
        elif direction == "right":
            return self.board[v_index][3 - e_index]
        elif direction == "up":
            return self.board[e_index][v_index]
        else:
            return self.board[3 - e_index][v_index]

    def update_vector(self, direction, index, vec):
        for i in range(4):
            self.update_element(direction, index, i, vec[i])

    def update_element(self, direction, v_index, e_index, value):
        if direction == "left":
            self.board[v_index][e_index] = value
        elif direction == "right":
            self.board[v_index][3 - e_index] = value
        elif direction == "up":
            self.board[e_index][v_index] = value
        else:
            self.board[3 - e_index][v_index] = value

    def can_move(self):
        # Determine the directions the board can currently move.
        result = []
        for dir in ["left", "right", "up", "down"]:
            if self.can_move_dir(dir):
                result.append(dir)
        return result

    def can_move_dir(self, direction):
        for index in range(4):
            row = self.vector(direction, index)
            row2 = next_row(row)
            if row != row2:
                return True
        return False

    def project(self, direction):
        # Create a new Board that moves the current
        # Board in the given direction.  This allows the next
        # state to be evaluated without messing up the "real"
        # board.
        result = Board()
        result.move_count = 0
        result.debugger = self.debugger
        result.board = deepcopy(self.board)
        points = result.move(direction)
        return result, points

    def best_move(self, directions):
        return max(self.evaluate(directions))[1]

    def evaluate(self, directions):
        # Determine the relative scores of moves in the different
        # directions.
        scores = []
        for direction in directions:
            board, points = self.project(direction)
            if self.debugger:
                print(f"\nevaluate {direction}:")
            total = board.score() + points
            if self.debugger:
                print(f"Total: {total}")
            scores.append((total, direction))
        return scores

    def score(self):
        # Heart of the recommendation logic.
        if self.debugger:
            self.display()
        cz = self.count_zeros()
        self.find_best_corners()
        bcs = self.best_corner_score()
        ns = self.old_neighbor_score()
        vs = self.vector_score()
        if self.debugger:
            print(f"count_zeros: {cz}")
            print(f"best_corner_score: {bcs}")
            print(f"neighbor_score: {ns}")
            print(f"vector_score: {vs}")
        return cz + bcs + ns + vs

    def find_best_corners(self):
        self.best_corners = []
        best_value = 0
        for i1 in [0, 3]:
            for i2 in [0, 3]:
                if self.board[i1][i2] > best_value:
                    self.best_corners = [(i1, i2)]
                    best_value = self.board[i1][i2]
                elif self.board[i1][2] == best_value:
                    self.best_corners.append((i1, i2))

    def best_corner_score(self):
        # Keeping the highest corner tile in the corner is
        # important so this gets a very high weight.
        if self.best_corners == []:
            return 0
        return self.element_value(self.best_corners[0]) * 16

    def element_value(self, element):
        # Elements are 2-tuples or None
        if element == None:
            return 0
        return self.board[element[0]][element[1]]

    def neighbor_score(self):
        result = 0
        for corner in self.best_corners:
            o0 = 1
            if corner[0] == 3:
                o0 = -1
            o1 = 1
            if corner[1] == 3:
                o1 = -1
            start_value = self.element_value(corner)
            value = self.path_value(start_value * 2, corner, (o0, 0), (0, o1))
            if value == None:
                value = 0
            value += self.locked(start_value, corner, (o0, 0), (0, o1))
            if value > result:
                result = value
        return result

    def locked(self, start_value, corner, d1, d2):
        if self.edge_locked(corner, d1) or self.edge_locked(start_value, corner, d2):
            return self.element_value(corner)
        return 0

    def edge_locked(self, start_value, corner, offset):
        element = corner
        value = start_value
        for i in range(3):
            element = tuple_sum(element, offset)
            next_value = self.element_value(element)
            if self.element_value(element) == 0 or value <= next_value:
                return False
            value = next_value
        return True

    def path_value(self, value, element, d1, d2):
        # if self.debugger:
        #     print(f"path_value: {value}, {element}, {d1}, {d2}")
        element_value = self.element_value(element)
        if element_value == 0:
            # if self.debugger:
            #     print(f"return {0}")
            return 0
        if element_value > value:
            # if self.debugger:
            #     print(f"return {None}")
            return None
        if element_value == value:
            # if self.debugger:
            #     print(f"return {value * 2}")
            return value * 2
        first_neighbor = tuple_sum(element, d1)
        first_value = None
        if valid_element(first_neighbor):
            first_value = self.path_value(element_value, first_neighbor, d1, d2)
            # if self.debugger:
            #     print(f"pop: {value}, {element}, {d1}, {d2}: {first_value}")
        else:
            d1 = (-d1[0], -d1[1])
        second_neighbor = tuple_sum(element, d2)
        second_value = None
        if valid_element(second_neighbor):
            second_value = self.path_value(element_value, second_neighbor, d1, d2)
            # if self.debugger:
            #     print(f"pop: {value}, {element}, {d1}, {d2}: {second_value}")
        if first_value == None:
            if second_value == None:
                result = None
            else:
                result = value + second_value
        elif second_value == None:
            result = value + first_value
        else:
            result = value + max([first_value, second_value])
        # if self.debugger:
        #     print(f"return {result}")
        return result

    def old_neighbor_score(self):
        # Calc best edge connected to the best_corner
        score = 0
        for corner in self.best_corners:
            offsets = self.neighbor_offsets(corner)
            for offset in offsets:
                score = max(score, self.edge_score(corner, offset))
        return score

    def edge_score(self, corner, offset):
        best_value = self.element_value(corner)
        neighbor = tuple_sum(corner, offset)
        neighbor_value = self.element_value(neighbor)
        if neighbor_value == 0 or neighbor_value > best_value:
            return 0
        result = neighbor_value * 4

        second_neighbor = tuple_sum(neighbor, offset)
        second_value = self.element_value(second_neighbor)
        if second_value == 0 or second_value > neighbor_value:
            return result
        result += second_value * 8

        third_neighbor = tuple_sum(second_neighbor, offset)
        third_value = self.element_value(third_neighbor)
        if third_value == 0 or third_value > second_value:
            return result
        return result + third_value * 8

    def neighbor_offsets(self, corner):
        result = []
        for o1, o2 in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            n1 = corner[0] + o1
            if n1 < 0 or n1 > 3:
                continue
            n2 = corner[1] + o2
            if n2 < 0 or n2 > 3:
                continue
            result.append((o1, o2))
        return result

    def vector_score(self):
        result = 0
        for i in range(4):
            for direction in ["left", "up"]:
                result += score_row(self.vector(direction, i))
        return result

    def init_stats(self):
        self.total_moves = 0
        self.total_sum = 0
        self.max_sum = 0
        self.min_sum = 2 << 16
        self.max_tile_count = {}
        self.worst_seed = 0

    def collect_stats(self):
        self.total_moves += self.move_count
        tiles = flatten(self.board)
        self.record_max_tile(max(tiles))
        tile_sum = sum(tiles)
        self.total_sum += tile_sum
        if tile_sum > self.max_sum:
            self.max_sum = tile_sum
            self.max_board = self.board
        if tile_sum < self.min_sum:
            self.min_sum = tile_sum
            self.worst_seed = self.seed

    def record_max_tile(self, tile):
        if tile in self.max_tile_count:
            self.max_tile_count[tile] += 1
        else:
            self.max_tile_count[tile] = 1

    def report_stats(self, count):
        print(f"Average moves: {self.total_moves/count}")
        print(f"Average sum: {self.total_sum/count}")
        print("Max tile distribution:")
        for key in sorted(self.max_tile_count.keys()):
            print(f"\t{key}: {self.max_tile_count[key]}")
        print(f"Max board: {self.max_board}")
        print(f"Worst seed: {self.worst_seed}")

    def run(self, count):
        self.init_stats()
        total_moves = 0
        total_sum = 0
        max_sum = 0
        for c in range(count):
            self.reset_board()
            moves = self.can_move()
            while moves != []:
                self.move(self.best_move(moves))
                self.add_tile()
                moves = self.can_move()
            self.collect_stats()
        self.report_stats(count)

    def make_recommendation(self, moves):
        print(f"Available moves: {moves}")
        scores = self.evaluate(moves)
        print(f"Scores: {scores}")
        result = max(scores)[1]
        print(f"Recommended move: {result}")
        return result
                
    def interactive(self):
        self.reset_board()
        print(self.seed)
        self.display()
        moves = self.can_move()
        keep_asking = True
        while moves != []:
            move = self.make_recommendation(moves)
            if keep_asking:
                command = input_move()
                if command != '':
                    if command == 'quit':
                        break
                    elif command == 'go':
                        keep_asking = False
                    elif command[0] == 's':
                        self.reset_board(int(move[1:]))
                        keep_asking = False
                    else:
                        move = command
            else:
                move = self.best_move(moves)
            if move not in moves:
                print(f"Invalid move: {move}")
                continue
            print(f"Moving {move}")
            self.move(move)
            self.add_tile()
            self.display()
            moves = self.can_move()
        self.report()

def valid_element(element):
    if element == None:
        return False
    return valid_index(element[0]) and valid_index(element[1])

def valid_index(index):
    return 0 <= index and index <= 3

def score_row(row):
    result = score_pairs(row)
    return score_pairs(row) - score_waves(row)

def score_pairs(row):
    result = 0
    prev = row[0]
    for element in row[1:]:
        if prev == element:
            result += element * 4
        prev = element
    return result

def score_waves(row):
    # waves (+,-,+ or -,+,- or +,-,+,- or -,+,-,+) are bad
    trim = [e for e in row if e != 0] # Remove 0s
    if len(trim) <= 2:
        return 0
    if trim[0] >= trim[1] and trim[1] >= trim[2]:
        trim.pop(0)
    elif trim[0] <= trim[1] and trim[1] <= trim[2]:
        trim.pop(0)
    if len(trim) <= 2:
        return 0
    if trim[-1] >= trim[-2] and trim[-2] >= trim[-3]:
        trim.pop()
    elif trim[-1] <= trim[-2] and trim[-2] <= trim[-3]:
        trim.pop(0)
    if len(trim) <= 2:
        return 0
    return sum(sorted(trim)[:-1])
    # result = sum(trim)
    # result -= max([trim[0], trim[-1]]) # Highest edge is ok
    # result += trim[1] # Double center
    # if len(trim) == 4:
    #     result += trim[2] # Double other center
    # return result


def no_zero(value):
    if value == 0:
        return ""
    return value

def row_points(row):
    result = 0
    prev = row[0]
    for element in row[1:]:
        if element == prev:
            result += element * 4
            prev = 0
        elif element != 0:
            prev = element
    return result
        
def next_row(row):
    result = [0, 0, 0, 0]
    remainder = row
    for index in range(4):
        result[index], remainder = next_element(remainder)
    return result

def next_element(remainder):
    previous_item = 0
    index = 0
    for item in remainder:
        index += 1
        if item != 0:
            if previous_item == item:
                return item * 2, remainder[index:]
            elif previous_item != 0:
                return previous_item, remainder[index-1:]
            previous_item = item
    return previous_item, []

def flatten(xss):
    return [x for xs in xss for x in xs]

def tuple_sum(t1, t2):
    if t1 == None:
        return None
    return tuple(map(lambda i, j: i + j, t1, t2))

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
