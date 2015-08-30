#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyogi.board import Board
from pyogi.plot import plot_board


if __name__ == '__main__':

    board = Board()
    board.set_initial_state()

    board.players = ['先手', '後手']

    board.move('+7776FU')
    board.move('-3334FU')
    board.move('+2868HI')
    board.move('-2288UM')
    board.move('+7988GI')

    # Plot by materials
    plot_board(board, savepath='example_pic.png', mode='pic')

    # Plot using matplotlib
    board.plot_state_mpl(figsize=(8, 9))
