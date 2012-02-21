#!/usr/bin/env python2

import sys
import time

import board
import player
import game

TERM_HOME = '\x1b[H'
TERM_CLEAR = '\x1b[2J'
TERM_CLEAR_LINE = '\x1b[2K'
TERM_HIDE_CURSOR = '\x1b[?25l'
TERM_SHOW_CURSOR = '\x1b[?25h'

class TermTron(object):
    def __init__(self, ais):
        self.tron = game.Tron((20, 78), ais)

    def draw_board(self, board, stream, highlight=[]):
        stream.write('#' * (board.columns + 2) + '\n')
        for rownum, row in enumerate(board.board, 1):
            stream.write('#')
            for colnum, cell in enumerate(row, 1):
                reset = False
                if (rownum, colnum) in highlight:
                    stream.write('\x1b[7m')
                    reset = True
                if cell:
                    reset = True
                    stream.write('\x1b[3%d;1m%s' % (int(cell)+1, cell))
                else:
                    stream.write('.')
                if reset:
                    stream.write('\x1b[0m')
            stream.write('#\n')
        stream.write('#' * (board.columns + 2) + '\n')

    def draw(self):
        sys.stdout.write(TERM_HOME)
        sys.stdout.write(TERM_CLEAR_LINE)
        sys.stdout.write('  %s\n' % self.status)
        self.draw_board(
                self.tron.board,
                sys.stdout,
                highlight=[p.position for p in self.tron.players])
        sys.stdout.flush()

    def setup_term(self):
        sys.stdout.write(TERM_CLEAR)
        sys.stdout.write(TERM_HIDE_CURSOR)

    def reset_term(self):
        sys.stdout.write(TERM_SHOW_CURSOR)
        sys.stdout.flush()

    def run(self):
        try:
            self.setup_term()
            while not self.tron.game_over:
                self.status = 'Turn %d.' % self.tron.turn
                self.tron.do_turn()
                self.draw()
            if self.tron.winner >= 0:
                self.status = 'Game over: %s won' % self.tron.players[self.tron.winner].name
            else:
                self.status = 'Game over.'
            self.draw()
            for p in self.tron.players:
                print '%s survived %d turns.' % (p.name, p.survived)
        finally:
            self.reset_term()


if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print 'Usage: %s AI [AI2 AI3 ...]' % sys.argv[0]
        sys.exit(1)
    ais = sys.argv[1:]
    TermTron(ais).run()
