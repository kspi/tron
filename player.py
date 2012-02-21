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
    def __init__(self, num, ai):
        self.alive = True
        self.survived = 0
        self.number = num
        self.name = 'Player %d' % num
        self.symbol = str(num)
        assert(len(self.symbol) == 1)
        self.ai = __import__('ai.%s' % ai, fromlist=['ai']).Agent()
    
    def move(self, board, players):
        action = self.ai.decide(board, players, self.number)
        self.direction = new_direction(self.direction, action)
        self.position = apply_direction(self.position, self.direction)
        if board.is_wall(self.position):
            self.alive = False
            return
        board.place_wall(self.position, self.symbol)
        self.survived += 1
