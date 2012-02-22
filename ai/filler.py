import player
from player import apply_direction, new_direction
import util

class Agent(object):
    def decide(self, board, players, num):
        me = players[num]

        forward = apply_direction(me.position, me.direction)
        if not board.is_wall(forward):
            return player.GO_FORWARD

        left_free = right_free = 0
        left = apply_direction(me.position, new_direction(me.direction, player.TURN_LEFT))
        if not board.is_wall(left):
            temp_board = board.copy()
            left_free = temp_board.fill(left)
        right = apply_direction(me.position, new_direction(me.direction, player.TURN_RIGHT))
        if not board.is_wall(right):
            temp_board = board.copy()
            right_free = temp_board.fill(right)

        if left_free > right_free:
            return player.TURN_LEFT
        else:
            return player.TURN_RIGHT
