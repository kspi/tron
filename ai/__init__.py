import player

class AIPlayer(player.Player):
    def __init__(self, ai):
        super(AIPlayer, self).__init__()
        self.ai = __import__('ai.%s' % ai, fromlist=['ai']).Agent()

    def decide(self, board, players):
        self.action = self.ai.decide(board, players, self.number)
