#!/usr/bin/env python2

import sys
import curses

import board
import player
import game
import ai
import util

ROWS = 24
COLUMNS = 80

class CursesTron(object):
    def __init__(self, args):
        players = []

        self.human = None
        self.human_delay = 200
        self.last_update = util.milliseconds()

        for arg in args:
            if arg == 'human':
                if self.human:
                    raise Exception('Only one human player allowed')
                self.human = player.Player()
                players.append(self.human)
            else:
                players.append(ai.AIPlayer(arg))
        self.tron = game.Tron((ROWS - 3, COLUMNS - 2), players)

    def draw(self, stdscr):
        stdscr.addstr(0, 4, self.status)
        stdscr.addstr(1, 0, '#' * COLUMNS)
        stdscr.addstr(ROWS - 1, 0, '#' * COLUMNS)
        for rownum, row in enumerate(self.tron.board.board, 1):
            stdscr.addstr(1 + rownum, 0, '#')
            stdscr.addstr(1 + rownum, COLUMNS - 1, '#')
            for colnum, cell in enumerate(row, 1):
                reset = False
                if cell:
                    stdscr.addstr(1 + rownum, colnum, '#', curses.A_BOLD | curses.color_pair(1 + int(cell)))
                else:
                    stdscr.addstr(1 + rownum, colnum, '.')
        for num, p in enumerate(self.tron.players):
            rownum, colnum = p.position
            if p.alive:
                symbol = ['^', '>', 'V', '<'][self.tron.players[num].direction]
            else:
                symbol = 'X'
            stdscr.addstr(1 + rownum, colnum, symbol, curses.A_BOLD | curses.A_REVERSE | curses.color_pair(1 + num))

        stdscr.refresh()

    def run(self):
        def run_wrapped(stdscr):
            curses.use_default_colors()
            curses.curs_set(0)
            stdscr.nodelay(1)

            curses.init_pair(1, curses.COLOR_BLUE, -1)
            curses.init_pair(2, curses.COLOR_RED, -1)
            curses.init_pair(3, curses.COLOR_GREEN, -1)
            curses.init_pair(4, curses.COLOR_YELLOW, -1)
            
            while not self.tron.game_over:
                self.status = 'Turn %d.' % self.tron.turn

                if self.human:
                    self.human.action = player.GO_FORWARD
                    now = util.milliseconds()
                    diff = now - self.last_update 
                    curses.napms(max(0, 200 - diff))
                    self.last_update = util.milliseconds()

                key = stdscr.getch()
                while key != -1:
                    if key == ord('q'):
                        sys.exit(0)
                    elif self.human:
                        if key in [ord(','), curses.KEY_LEFT]:
                            self.human.action = player.TURN_LEFT
                        elif key in [ord('.'), curses.KEY_RIGHT]:
                            self.human.action = player.TURN_RIGHT
                    key = stdscr.getch()
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
        print 'Usage: %s PLAYER [PLAYER2 PLAYER3 ...]' % sys.argv[0]
        print 'Here, PLAYER is either "human" or an AI module name.'
        sys.exit(1)
    args = sys.argv[1:]
    CursesTron(args).run()

