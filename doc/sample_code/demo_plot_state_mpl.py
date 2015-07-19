#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
demo using pyogi.board.plot_state_mpl()
'''

import sys
sys.path.append('./../../')

from pyogi.board import *


if __name__ == '__main__':
    board = Board()
    board.set_initial_state()

    board.players = ['先手', '後手']

    board.move('+7776FU')
    board.move('-3334FU')
    board.move('+2868HI')
    board.move('-2288UM')

    board.plot_state_mpl(figsize=(8, 9))
