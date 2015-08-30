#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .picplot import plot_state_pic
from .mplplot import plot_state_mpl


def plot_board(board, savepath=None, title='', mode='pic', last_move_xy=None, figsize=None):
    '''Plot board object
    '''
    if mode == 'pic':
        plot_state_pic(board, savepath)
    elif mode == 'mpl':
        plot_state_mpl(board, figsize=figsize, savepath=savepath,
                       title=title, last_move_xy=last_move_xy)
    else:
        print('Invalid mode : {0}'.format(mode))
