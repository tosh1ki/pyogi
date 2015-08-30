#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
font = {'family': 'TakaoGothic'}
matplotlib.rc('font', **font)


board_indexes = list(range(0, 9))


def plot_state_mpl(board, savepath=None, title='', last_move_xy=None, figsize=(8, 9)):
    mplplot = MplPlot(board, figsize=figsize, title=title, last_move_xy=last_move_xy)
    mplplot.plot()

    if savepath:
        mplplot.save(savepath)

    mplplot.show()


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
