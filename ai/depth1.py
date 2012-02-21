import player
from player import apply_direction, new_direction
import util

class Agent(object):
    def decide(self, board, players, num):
        me = players[num]
        forward = apply_direction(me.position, me.direction)
        f = not board.is_wall(forward)
        left = apply_direction(me.position, new_direction(me.direction, player.TURN_LEFT))
        l = not board.is_wall(left)
        right = apply_direction(me.position, new_direction(me.direction, player.TURN_RIGHT))
        r = not board.is_wall(right)

        if f and l and r:
            return util.choose_randomly([
                (0.001, player.TURN_LEFT),
                (0.998, player.GO_FORWARD),
                (0.001, player.TURN_RIGHT),
            ])
        elif f and l or f and r:
            return util.choose_randomly([
                (0.999, player.GO_FORWARD),
                (0.001, player.TURN_LEFT if l else player.TURN_RIGHT),
            ])
        elif l and r:
            return util.choose_randomly([
                (0.5, player.TURN_LEFT),
                (0.5, player.TURN_RIGHT),
            ])
        elif l:
            return player.TURN_LEFT
        elif r:
            return player.TURN_RIGHT
        else:
            return player.GO_FORWARD
