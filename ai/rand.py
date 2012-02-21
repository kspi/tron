import player
import util

class Agent(object):
    def decide(self, board, me, her):
        return util.choose_randomly([
            (0.2, player.TURN_LEFT),
            (0.6, player.GO_FORWARD),
            (0.2, player.TURN_RIGHT),
        ])
