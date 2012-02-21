import player
from player import apply_direction, new_direction
import util
from collections import namedtuple

SimplePlayer = namedtuple('SimplePlayer', 'direction position')

OUTCOME_TYPES = UNDEFINED, LOSE, UNKNOWN, WIN = range(4)

def outcome_lose(iterations):
    return (LOSE, iterations)

def outcome_unknown(my_space, opponents_space):
    return (UNKNOWN, my_space, opponents_space)

def outcome_win(iterations):
    return (WIN, iterations)

def invert_outcome(outcome):
    if outcome[0] == LOSE:
        return (WIN, outcome[1])
    elif outcome[0] == UNKNOWN:
        return (UNKNOWN, outcome[2], outcome[1])
    elif outcome[0] == WIN:
        return (LOSE, outcome[1])
    else:
        return outcome

class Agent(object):
    def __init__(self):
        self.depth = 3
        self.my_space_importance = 1
        self.opponents_space_importance = 1

    def decide(self, board, players, num):
        # We'll be mutating the board.
        new_board = board.copy() 

        if len(players) != 2:
            raise Exception('The minmax AI only supports 2-player games.')

        # The minmax procedure expects the current player to always be the head of the list.
        rotated_players = util.list_rotated_left(players, amount=num)
        simple_players = [SimplePlayer(p.direction, p.position) for p in rotated_players]

        action, outcome = self.minmax(new_board, simple_players, 0)

        return action

    def compare_outcomes(self, a, b):
        if a[0] == b[0]:
            if a[0] == LOSE:
                return cmp(a[1], b[1])
            elif a[0] == UNKNOWN:
                a_val = (a[1] * self.my_space_importance -
                         a[2] * self.opponents_space_importance)
                b_val = (b[1] * self.my_space_importance -
                         b[2] * self.opponents_space_importance)
                return cmp(a_val, b_val)
            elif a[0] == WIN:
                return -cmp(a[1], b[1])
            else:
                return 0
        else:
            return cmp(a[0], b[0])

    def minmax(self, board, players, iteration):
        me, opponent = players
        if iteration < self.depth:
            best_outcome = (UNDEFINED,)
            best_action = None
            for action in [player.GO_FORWARD, player.TURN_LEFT, player.TURN_RIGHT]:
                new_dir = new_direction(me.direction, action)
                new_pos = apply_direction(me.position, new_dir)
                if board.is_wall(new_pos):
                    outcome = outcome_lose(iteration)
                else:
                    board.place_wall(new_pos)
                    new_me = SimplePlayer(new_dir, new_pos)
                    opponents_action, opponents_outcome = self.minmax(board, (opponent, new_me), iteration + 1)
                    outcome = invert_outcome(opponents_outcome)
                    board.remove_wall(new_pos)
                if self.compare_outcomes(outcome, best_outcome) > 0:
                    best_outcome = outcome
                    best_action = action
            return (best_action, best_outcome)
        else:
            temp_board = board.copy()
            temp_board.remove_wall(me.position)
            temp_board.remove_wall(opponent.position)
            my_space = temp_board.fill(me.position)
            opponents_space = temp_board.fill(opponent.position)
            if opponents_space == 0:
                opponents_space == my_space
            return player.GO_FORWARD, outcome_unknown(my_space, opponents_space)

