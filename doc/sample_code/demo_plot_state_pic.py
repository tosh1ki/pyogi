#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('./../../')
from pyogi.board import Board
from pyogi.board import initial_state_csa
from pyogi.plot import plot_board_pic


if __name__ == '__main__':

    board = Board()
    board.set_initial_state()

    board.players = ['先手', '後手']

    board.move('+7776FU')
    board.move('-3334FU')
    board.move('+2868HI')
    board.move('-2288UM')
    board.move('+7988GI')

    path_materials = './../../pyogi/materials/'

    plot_board_pic(board, path_materials)
