#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
demo using pyogi.board.plot_state_mpl()
'''

import sys
sys.path.append('./../')

from pyogi.board import *


if __name__ == '__main__':
    board = Board()
    board.set_initial_state()

    board.move('+7776FU')
    board.move('-3334FU')
    board.move('+2868HI')

    board.plot_state_mpl(title='角交換四間飛車')
