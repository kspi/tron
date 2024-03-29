import board

# Directions
DIRECTIONS = NORTH, EAST, SOUTH, WEST = range(4)

# Actions
ACTIONS = TURN_LEFT, GO_FORWARD, TURN_RIGHT = -1, 0, 1

PLAYER_OFFSET = 4


def direction_delta(d):
    return {
        NORTH: (-1, 0),
        EAST: (0, 1),
        SOUTH: (1, 0),
        WEST: (0, -1),
    }[d]


def new_direction(d, action):
    return (d + action) % 4


def add_positions(a, b):
    return tuple(map(lambda x, y: x + y, a, b))

def apply_direction(position, d):
    return add_positions(position, direction_delta(d))


class Player(object):
    def __init__(self):
        self.alive = True
        self.survived = 0
        self.action = GO_FORWARD

    def setup(self, num):
        self.number = num
        self.name = 'Player %d' % num
        self.symbol = str(num)
    
    def decide(self, board, players):
        pass

    def move(self, board):
        self.direction = new_direction(self.direction, self.action)
        new_position = apply_direction(self.position, self.direction)
        if board.is_wall(new_position):
            self.alive = False
        else:
            self.position = new_position
            board.place_wall(self.position, self.symbol)
            self.survived += 1
