#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import gridspec

sys.path.append('./../../')
from pyogi.board import Board
from pyogi.board import initial_state_csa


csa_to_code = {
    'OU': 1, 'HI': 2, 'KA': 3, 'KI': 4, 'GI': 5,
    'KE': 6, 'KY': 7, 'FU': 8, 'RY': 22, 'UM': 23,
    'NG': 24, 'NK': 26, 'NY': 27, 'TO': 28
}


def plot_state_pic(pieces_list, mochigoma_list, path_materials):

    fig = plt.figure(figsize=(8, 8))

    gs = gridspec.GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[1, 1])
    plt.subplots_adjust(wspace=0.05, hspace=0.05)

    ax1 = plt.subplot(gs[0:2, 0])
    ax20 = plt.subplot(gs[0, 1])
    ax21 = plt.subplot(gs[1, 1])

    for ax in [ax1, ax20, ax21]:
        ax.tick_params(
            labelleft='off', labelbottom='off',
            bottom='off', top='off', left='off', right='off'
        )

    # Plot a board
    path_jpg = os.path.join(path_materials, 'japanese-chess-b02.jpg')
    img = mpimg.imread(path_jpg)


    ax1.imshow(img, extent=[0, 10, 0, 10])


    # Plot pieces on a board
    for which, i, j, csa in pieces_list:
        is_gote = which == '-'
        koma_code = is_gote*30 + csa_to_code[csa]

        fname = 'sgl{0:02}.png'.format(koma_code)
        path_koma = os.path.join(path_materials, fname)
        img_koma = mpimg.imread(path_koma)
        ax1.autoscale(False)
        x, y = 0.5 + (9 - i), 0.5 + (9 - j)
        ax1.imshow(img_koma, extent=[x, x+1, y, y+1])

    # Plot koma-dai
    fname = 'japanese-chess-bg.jpg'
    path = os.path.join(path_materials, fname)
    img = mpimg.imread(path)

    axes = [ax21, ax20]
    for ax in axes:
        ax.autoscale(False)
        ax.imshow(img, extent=[0, 5, 0, 5])

    # Plot mochigoma
    n_sente_mochigoma = 0
    n_gote_mochigoma = 0
    
    for which, csa in mochigoma_list:
        is_gote = which == '-'

        koma_code = 30*is_gote + csa_to_code[csa]
        fname = 'sgl{0:02}.png'.format(koma_code)
        path_koma = os.path.join(path_materials, fname)
        img_koma = mpimg.imread(path_koma)
        axes[is_gote].autoscale(False)

        if not is_gote:
            x = 1/9 * float(n_sente_mochigoma % 7)
            y = 0.28 * float(n_sente_mochigoma // 7)
        else:
            x = 1/9 * float(n_gote_mochigoma % 7)
            y = (1 - 1/4) - 0.28 * float(n_gote_mochigoma // 7)

        axes[is_gote].imshow(img_koma, extent=[x, x+1/4, y, y+1/4])

        n_sente_mochigoma += not is_gote
        n_gote_mochigoma += is_gote

    plt.show()


def plot_board_pic(board, path_materials):
    '''Plot board object
    '''

    pieces_list = []
    for i, row in enumerate(board.board):
        for j, grid in enumerate(row):
            if grid.which_player != ' ':
                pieces_list.append((grid.which_player, i+1, j+1, grid.koma.csa))
    
    mochigoma_list = []
    for i, _mochigoma_list in enumerate(board.mochigoma):
        if i == 0:
            which_player = '+'
        else:
            which_player = '-'

        for _mochigoma in _mochigoma_list:
            mochigoma_list.append((which_player, _mochigoma.csa))


    plot_state_pic(pieces_list, mochigoma_list, path_materials)



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
