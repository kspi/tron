#!/usr/bin/env python2

import sys

import game

if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print 'Usage: %s ROWS COLUMNS AI [AI2 AI3 ...]' % sys.argv[0]
        sys.exit(1)
    rows = int(sys.argv[1])
    columns = int(sys.argv[2])
    ais = sys.argv[3:]
    tron = game.Tron((rows, columns), ais)
    winner = tron.run()
    print '%s won after %d turns.' % (tron.players[winner].name, tron.turn)
