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

    board.move('+7776FU')
    board.move('-3334FU')
    board.move('+2868HI')
    board.move('-2288UM')
    board.move('+7988GI')

    print(board)
    board.plot_state_mpl(sente_name='先手の人', gote_name='後手の人',
                         savepath='kk4.png')
