class Projection:
    def __init__(self, board, points, weight):
        self.board = board
        self.points = points
        self.weight = weight

    def weighted_total(self):
        if self.points == None: # GAME OVER
            return -self.board.total_sum()
        return (self.points + self.board.score()) * self.weight

