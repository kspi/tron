import board
import player

class Tron(object):
    def __init__(self, board_size, players):
        self.game_over = False
        self.winner = -1
        self.turn = 0
        self.board = board.Board(board_size)
        
        self.players = players
        player_offset_col = 5
        player_offset_row = self.board.rows / len(self.players)
        if player_offset_row == 0:
            raise Exception('Too many players.')
        for num, p in enumerate(self.players):
            p.setup(num)
            if num % 2 == 0:
                p.position = (player_offset_row * (1 + num / 2), player_offset_col)
                pos_dir = 1
                p.direction = player.EAST
            elif num % 2 == 1:
                p.position = (self.board.rows - player_offset_row * (1 + num / 2) + 1, self.board.columns - player_offset_col + 1)
                pos_dir = -1
                p.direction = player.WEST


    def check_winning_condition(self):
        if len(self.players) == 1:
            self.game_over = not self.players[0].alive
        else:
            alive_count = 0
            last_alive = None
            for i, p in enumerate(self.players):
                if p.alive:
                    alive_count += 1
                    last_alive = i
            if alive_count == 1:
                self.game_over = True
                self.winner = last_alive

    def do_turn(self):
        self.turn += 1
        for num, player in enumerate(self.players):
            if player.alive:
                player.decide(self.board, self.players)
                player.move(self.board)
                self.check_winning_condition()
                if self.game_over:
                    return 

    def run(self):
        while not self.game_over:
            self.do_turn()
        return self.winner
