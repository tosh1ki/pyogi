#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
font = {'family': 'TakaoGothic'}
matplotlib.rc('font', **font)

import matplotlib.image as mpimg
from matplotlib import gridspec

PATH_MATERIALS = os.path.join(os.path.dirname(__file__), 'materials')
csa_to_code = {
    'OU': 1, 'HI': 2, 'KA': 3, 'KI': 4, 'GI': 5,
    'KE': 6, 'KY': 7, 'FU': 8, 'RY': 22, 'UM': 23,
    'NG': 24, 'NK': 26, 'NY': 27, 'TO': 28
}
board_indexes = list(range(0, 9))



class PicPlot:
    def __init__(self, pieces_list, mochigoma_list):
        self.pieces_list = pieces_list
        self.mochigoma_list = mochigoma_list

        fig = plt.figure(figsize=(8, 8))

        gs = gridspec.GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[1, 1])
        plt.subplots_adjust(wspace=0.05, hspace=0.05)

        self.ax1 = plt.subplot(gs[0:2, 0])
        self.ax20 = plt.subplot(gs[0, 1])
        self.ax21 = plt.subplot(gs[1, 1])

        # Initialize subplots
        for ax in [self.ax1, self.ax20, self.ax21]:
            ax.tick_params(
                labelleft='off', labelbottom='off',
                bottom='off', top='off', left='off', right='off'
            )

    def plot(self):
        self.plot_board()
        self.plot_pieces()
        self.plot_komadai()
        self.plot_mochigoma()

    def plot_board(self):
        path_jpg = os.path.join(PATH_MATERIALS, 'japanese-chess-b02.jpg')
        img = mpimg.imread(path_jpg)

        self.ax1.imshow(img, extent=[0, 10, 0, 10])

    def plot_pieces(self):
        for which, i, j, csa in self.pieces_list:
            is_gote = which == '-'
            koma_code = is_gote*30 + csa_to_code[csa]

            fname = 'sgl{0:02}.png'.format(koma_code)
            path_koma = os.path.join(PATH_MATERIALS, fname)
            img_koma = mpimg.imread(path_koma)

            self.ax1.autoscale(False)
            x, y = 0.5 + (9 - i), 0.5 + (9 - j)
            self.ax1.imshow(img_koma, extent=[x, x+1, y, y+1])

    def plot_komadai(self):
        fname = 'japanese-chess-bg.jpg'
        path = os.path.join(PATH_MATERIALS, fname)
        img = mpimg.imread(path)

        axes = [self.ax21, self.ax20]
        for ax in axes:
            ax.autoscale(False)
            ax.imshow(img, extent=[0, 5, 0, 5])

    def plot_mochigoma(self):
        n_sente_mochigoma = 0
        n_gote_mochigoma = 0

        axes = [self.ax21, self.ax20]
    
        for which, csa in self.mochigoma_list:
            is_gote = which == '-'

            koma_code = 30*is_gote + csa_to_code[csa]
            fname = 'sgl{0:02}.png'.format(koma_code)
            path_koma = os.path.join(PATH_MATERIALS, fname)
            img_koma = mpimg.imread(path_koma)
            axes[is_gote].autoscale(False)

            N_COLUMN = 9
            
            if not is_gote:
                x = 0.1 * float(n_sente_mochigoma % N_COLUMN)
                y = 0.2 * float(n_sente_mochigoma // N_COLUMN)
            else:
                x = 0.1 * float(n_gote_mochigoma % N_COLUMN)
                y = (1 - 0.25) - 0.2 * float(n_gote_mochigoma // N_COLUMN)

            axes[is_gote].imshow(img_koma, extent=[x, x+1/5, y, y+1/5])

            n_sente_mochigoma += not is_gote
            n_gote_mochigoma += is_gote

    def save(self, savepath):
        plt.savefig(savepath, bbox_inches="tight", pad_inches=0.0)

    def show(self):
        plt.show()


class MplPlot(object):
    def __init__(self, board, figsize=(8, 9), title='', last_move_xy=None):
        self.board = board
        self.title = title
        self.last_move_xy = last_move_xy

        _, self.ax = plt.subplots(figsize=figsize)

        self.width_x = figsize[0]
        self.width_y = figsize[1]

        plt.xlim(0, self.width_x)
        plt.ylim(0, self.width_y)

        self.dx = self.width_x / 9
        self.dy = self.width_y / 9

        self.fontsize = 30 * min(self.dx, self.dy)

    def plot(self):
        self.plot_grid()
        self.plot_pch()
        self.plot_pieces()
        self.plot_mochigoma()
        self.plot_names()
        self.plot_title(self.title)

    def plot_grid(self):
        for i in range(1, 9):
            x = i * self.dx
            y = i * self.dy
            plt.plot([0, self.width_x], [y, y], color='black')
            plt.plot([x, x], [0, self.width_y], color='black')

    def plot_pch(self):
        for x in [3 * self.dx, 6 * self.dx]:
            for y in [3 * self.dy, 6 * self.dy]:
                plt.plot([x], [y],
                         marker='o', color='black', linestyle='None')

    def plot_pieces(self):
        for j in board_indexes:
            for i, b_i in enumerate(board_indexes):
                grid = self.board[b_i][j]

                x = ((8 - i) + 0.5) * self.dx
                y = ((8 - j) + 0.5) * self.dy

                if not grid.is_empty():
                    is_gote = not grid.is_of_sente()

                    # TOFIX: 60, 80にするとよくわからないけどうまくいく
                    plt.text(x - self.fontsize / 2 / 60, 
                             y - self.fontsize / 2 / 80,
                             grid.koma.kanji,
                             size=self.fontsize, rotation=180 * is_gote)
                    
                # Plot circle around piece moved recently
                if (self.last_move_xy and
                    len(self.last_move_xy) == 2 and
                    self.last_move_xy[0] == i and
                    self.last_move_xy[1] == j):
                    circle = Circle(
                        (x, y), 0.5 * self.dx, facecolor='none',
                        linewidth=3, alpha=0.5)
                    self.ax.add_patch(circle)

    def plot_mochigoma(self):
        plt.text(0, -0.5 * self.dx, self.board.get_mochigoma_str(0),
                 fontsize=self.fontsize)
        plt.text(0,  9.2 * self.dy, self.board.get_mochigoma_str(1),
                 fontsize=self.fontsize, rotation=180)

    def plot_names(self):
        plt.text(self.width_x + 0.2, 2 * self.dy, self.board.players[0],
                 fontsize=self.fontsize, rotation=90)
        plt.text(self.width_x + 0.2, 8 * self.dy, self.board.players[1],
                 fontsize=self.fontsize, rotation=90)

    def plot_title(self, title):
        plt.title(title, y=1.07, fontsize=self.fontsize)
        plt.tick_params(labelleft='off', labelbottom='off')

    def save(self, savepath):
        plt.savefig(savepath)
    
    def show(self):
        plt.show()


def plot_state_pic(board, savepath=None):
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


    picplot = PicPlot(pieces_list, mochigoma_list)
    picplot.plot()

    if savepath:
        picplot.save(savepath)

    picplot.show()

def plot_state_mpl(board, savepath=None, title='', last_move_xy=None, figsize=(8, 9)):
    mplplot = MplPlot(board, figsize=figsize, title=title, last_move_xy=last_move_xy)
    mplplot.plot()

    if savepath:
        mplplot.save(savepath)

    mplplot.show()

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
