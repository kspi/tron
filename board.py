import player

class Board(object):
    def __init__(self, size):
        self.size = size
        self.rows, self.columns = size
        self.board = [[False for col in range(self.columns)]
                      for row in range(self.rows)]
        
    def in_bounds(self, position):
        row, col = position
        return 1 <= row <= self.rows and 1 <= col <= self.columns

    def place_wall(self, position, kind='#'):
        assert(self.in_bounds(position))
        row, col = position
        self.board[row - 1][col - 1] = kind

    def remove_wall(self, position):
        assert(self.in_bounds(position))
        row, col = position
        self.board[row - 1][col - 1] = False

    def is_wall(self, position):
        if not self.in_bounds(position):
            return '#'
        else:
            row, col = position
            return self.board[row - 1][col - 1]

    def copy(self):
        new_board = Board(self.size)
        for row in range(self.rows):
            for col in range(self.columns):
                new_board.board[row][col] = self.board[row][col]
        return new_board

    def fill(self, position):
        queue = [position]
        filled = 0
        while queue:
            pos = queue.pop(0)
            if not self.is_wall(pos):
                self.place_wall(pos)
                filled += 1
                for d in player.DIRECTIONS:
                    p = player.apply_direction(pos, d)
                    queue.append(p)
        return filled
