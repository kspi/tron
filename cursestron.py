#!/usr/bin/env python2

import sys
import time
import curses

import board
import player
import game

ROWS = 24
COLUMNS = 80

class CursesTron(object):
    def __init__(self, ais):
        self.tron = game.Tron((ROWS - 3, COLUMNS - 2), ais)

    def draw(self, stdscr):
        highlight = [p.position for p in self.tron.players] 
        stdscr.addstr(0, 4, self.status)
        stdscr.addstr(1, 0, '#' * COLUMNS)
        stdscr.addstr(ROWS - 1, 0, '#' * COLUMNS)
        for rownum, row in enumerate(self.tron.board.board, 1):
            stdscr.addstr(1 + rownum, 0, '#')
            stdscr.addstr(1 + rownum, COLUMNS - 1, '#')
            for colnum, cell in enumerate(row, 1):
                reset = False
                if (rownum, colnum) in highlight:
                    num = int(cell)
                    symbol = ['^', '>', 'V', '<'][self.tron.players[num].direction]
                    stdscr.addstr(1 + rownum, colnum, symbol, curses.A_BOLD | curses.A_REVERSE | curses.color_pair(1 + num))
                elif cell:
                    stdscr.addstr(1 + rownum, colnum, '#', curses.A_BOLD | curses.color_pair(1 + int(cell)))
                else:
                    stdscr.addstr(1 + rownum, colnum, '.')
        stdscr.refresh()

    def run(self):
        def run_wrapped(stdscr):
            curses.use_default_colors()
            curses.curs_set(0)

            curses.init_pair(1, curses.COLOR_BLUE, -1)
            curses.init_pair(2, curses.COLOR_RED, -1)
            curses.init_pair(3, curses.COLOR_GREEN, -1)
            curses.init_pair(4, curses.COLOR_YELLOW, -1)
            
            while not self.tron.game_over:
                self.status = 'Turn %d.' % self.tron.turn
                self.tron.do_turn()
                self.draw(stdscr)
            if self.tron.winner >= 0:
                self.status = 'Game over: %s won' % self.tron.players[self.tron.winner].name
            else:
                self.status = 'Game over.'
            self.draw(stdscr)

            for num, p in enumerate(self.tron.players):
                stdscr.addstr(ROWS + num, 4, '%s survived %d turns.' % (p.name, p.survived))

            stdscr.nodelay(0)
            stdscr.getch()
        curses.wrapper(run_wrapped)


if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print 'Usage: %s AI [AI2 AI3 ...]' % sys.argv[0]
        sys.exit(1)
    ais = sys.argv[1:]
    CursesTron(ais).run()

