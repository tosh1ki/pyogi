#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
font = {'family': 'TakaoGothic'}
matplotlib.rc('font', **font)

import pdb

from .pieces_act import *

EMPTY_STR = '   '
all_mochigoma = ['FU'] * 9 + ['KI', 'GI', 'KE', 'KY'] * 2 + ['HI', 'KA', 'OU']
board_indexes = list(range(0, 9))
TEBAN_CODE = ['+', '-']
KOMAOCHI_OPTIONS = {
    'hirate': [],
    'kakuoti': ['22KA'],
    'hisyaoti': ['82HI'],
    'kyouoti': ['11KY'],
    'migikyouoti': ['91KY'],
    'hikyouoti': ['82HI', '11KY'],
    'nimaioti': ['82HI', '22KA'],
    'sanmaioti': ['82HI', '22KA', '11KY'],
    'yonmaioti': ['91KY', '82HI', '22KA', '11KY'],
    'rokumaioti': ['91KY', '81KE', '82HI', '22KA', '21KE', '11KY']
}


class Board:

    '''Shogi board class

    Member variables
    -------------------
    Board.board : list (two-dimensional array, 9 x 9)
        If you want to access a piece as '7六',
        >>> print(board[6][5])
    Board.mochigoma : list
        mochigoma list

    Examples
    -------------------
    >>> board = Board()
    >>> board.set_initial_state()
    >>> board.move('+7776FU')
    >>> board.move('-3334FU')
    >>> board.move('+8822UM')
    >>> board.move('-3122GI')
    >>> print(board)
    '''

    def __init__(self):
        self.board = [[EMPTY_STR] * 9 for n in range(9)]
        self.mochigoma = [[], []]
        self.tesu = 0
        self.last_move_txt = ''
        self.last_move_xy = []
        self.teai = ''

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        row_separator = '-' * 37

        sente_mochigoma = self.get_mochigoma_str(0, kanji=False)
        gote_mochigoma = self.get_mochigoma_str(1, kanji=False)

        s = ['{}手目: {}'.format(self.tesu, self.last_move_txt),
             gote_mochigoma, row_separator]

        for j in board_indexes:
            s_j = []
            for i in board_indexes[::-1]:
                s_ij = ''.join(self.board[i][j])
                s_j.append(s_ij)

            s_temp = '|' + '|'.join(s_j) + '|'
            s.append(s_temp)
            s.append(row_separator)

        s.append(sente_mochigoma)  # sente's mochigoma

        return '\n'.join(s)

    def plot_state_mpl(self, figsize=(8, 9), title = '', savepath=None):
        '''Plot current state using matplotlib.
        '''
        fig, ax = plt.subplots(figsize=figsize)

        width_x = 9
        width_y = 9

        plt.xlim(0, width_x)
        plt.ylim(0, width_y)

        dx = width_x / 9
        dy = width_y / 9

        fontsize = 20 * dx

        # Plot grids
        for i in range(1, 9):
            x = i * dx
            y = i * dy
            plt.plot([0, width_x], [y, y], color='black')
            plt.plot([x, x], [0, width_y], color='black')

        # Plot pch
        for x in [3 * dx, 6 * dx]:
            for y in [3 * dy, 6 * dy]:
                plt.plot([x], [y],
                         marker='o', color='black', linestyle='None')

        # Plot pieces
        for j in board_indexes:
            for i, b_i in enumerate(board_indexes):
                d = self.board[b_i][j]

                x = (8 - i) + dx / 2
                y = (8 - j) + dy / 2

                if d != EMPTY_STR:
                    s = CSA_TO_KANJI[d[1]]
                    is_gote = int(d[0] == '-')
                    plt.text(x - 1 / 5, y - 1 / 10, s,
                             size=fontsize, rotation=180 * is_gote)

                # Plot circle around piece moved recently
                if (len(self.last_move_xy) == 2 and
                        self.last_move_xy[0] == i and
                        self.last_move_xy[1] == j):
                    circle = Circle((x, y), 0.5, facecolor='none',
                                    linewidth=3, alpha=0.5)
                    ax.add_patch(circle)

        # Plot mochigoma
        plt.text(0, -0.5 * dx, self.get_mochigoma_str(0),
                 fontsize=fontsize)
        plt.text(0,  9.2 * dy, self.get_mochigoma_str(1),
                 fontsize=fontsize, rotation=180)

        # Plot title
        plt.title(title, y=1.07, fontsize=fontsize)
        plt.tick_params(labelleft='off', labelbottom='off')

        if savepath:
            fig.savefig(savepath)
        else:
            plt.show()

    def get_mochigoma_str(self, teban, kanji=True):
        '''Returns string of all mochigoma.

        teban : int
            0 : sente
            1 : gote
        '''
        if kanji:
            mochigoma = map(lambda x: CSA_TO_KANJI[x], self.mochigoma[teban])
            koma = KOMA_KANJI
        else:
            mochigoma = self.mochigoma[teban]
            koma = KOMA_CSA

        counter = Counter(mochigoma)
        mochigoma_list = []

        for k in koma:
            if counter[k] == 1:
                mochigoma_list.append(k)
            elif counter[k] > 1:
                mochigoma_list.append('{0}x{1}'.format(k, counter[k]))

        return ' '.join(mochigoma_list)

    def __setitem__(self, index, value):
        self.board[index] = value

    def __getitem__(self, index):
        return self.board[index]

    def set_initial_state(self, teai='hirate'):
        '''Set state as initial state (with handicap).

        Args
        -------------------
        teai : str, optional (default = 'hirate')
            Type of komaoti (handicap)
            ex. hirate, kakuoti, hisyaoti, kyouoti,migikyouoti,
                hikyouoti, nimaioti, sanmaioti, yonmaioti, rokumaioti
        '''
        self.mochigoma = [list(all_mochigoma), list(all_mochigoma)]

        curdir = os.path.dirname(__file__)

        csapath = os.path.join(curdir, 'initial_state_hirate.csa')
        with open(csapath, 'r') as f:
            initial_csa = f.read()

        moves = initial_csa.split('\n')

        for move in moves:
            if move:
                self.move(move)

        # Komaochi
        for d_teai, d_pieces in KOMAOCHI_OPTIONS.items():
            if teai == d_teai:
                delete_piece = d_pieces
                break
        else:
            raise RuntimeError('invalid teai', teai)

        for dp in delete_piece:
            i = int(dp[0]) - 1
            j = int(dp[1]) - 1
            p = dp[2:]

            if self[i][j] == ['-', p]:
                self[i][j] = EMPTY_STR

        self.last_move_txt = ''
        self.last_move_xy = []
        self.tesu = 0
        self.teai = teai

    def move(self, move):
        '''Move a piece on a board

        Args
        -------------------
        move : str
            Move CSA format
            ex. '+9998KY'
        '''
        teban = int(move[0] != '+')  # 0 if sente, 1 if gote

        points = list(map(int, list(move[1:5])))
        prev_point = points[0:2]
        next_point = points[2:4]
        koma = move[5:]

        picked_koma = ''

        if prev_point == [0, 0]:
            # use mochigoma
            self.mochigoma[teban].remove(koma)
        else:
            self.board[prev_point[0] - 1][prev_point[1] - 1] = EMPTY_STR

        next_point_info = self.board[next_point[0] - 1][next_point[1] - 1]

        # If picking enemy's koma
        if next_point_info != EMPTY_STR:
            picked_koma = next_point_info[1]

            # If picking promoted piece
            if picked_koma in TURN_PIECE:
                picked_koma = TURN_PIECE[picked_koma]

            self.mochigoma[teban].append(picked_koma)

        moved_koma = [move[0], koma]
        self.board[next_point[0] - 1][next_point[1] - 1] = moved_koma

        self.last_move_txt = move
        self.last_move_xy = [next_point[0] - 1, next_point[1] - 1]
        self.tesu += 1

        return [moved_koma, picked_koma]

    def get_piece_indexes(self, piece):
        '''Get indexes of a certain piece on a board.

        Args
        -------------------
        piece : str
           which piece you want to search.
            ex. 'KA'

        Returns
        -------------------
        (at initial state)
        >>> board.get_piece_indexes('HI')
        [[[7, 1]], [[1, 7]]]
        '''
        pieces_index = [[], []]
        for j, column in enumerate(self.board):
            for i, value in enumerate(column):
                teban = value[0]
                board_piece = value[1]
                if board_piece == piece:
                    pieces_index[teban==TEBAN_CODE[1]].append([j, i])

        return pieces_index

    def is_forking(self, targets=['OU', 'HI'], display=True):
        '''Check that there is an piece which forked by enemy's piece.
        Search a state that one of all pieces forks all pieces of `target` at.

        Args
        -------------------
        target : list
            ex. ['OU', 'HI']
        display : bool, optional (default = True)
            If True, display state that forked.

        Returns
        -------------------
        is_forked_list : list of True/False
            is_forked_list[0] : Is sente's piece forked?
            is_forked_list[1] : Is  gote's piece forked?
        '''
        results = [False, False]

        for query_piece in ALL_KOMA:
            results_tmp = self.is_forking_query(query_piece, targets, display)
            results = [results[0] or results_tmp[0],
                       results[1] or results_tmp[1]]

        return results

    def is_forking_query(self, query_piece, targets, display=True):
        '''Check that there is a piece which forked by enemy's piece.
        Search a state which `query_piece` forks all pieces of `target` at.

        Args
        -------------------
        query_piece : str
            ex. 'KA'
        target : list
            Check whether pieces of `target` are forked or not.
            ex. ['OU', 'HI']
        display : bool, optional (default = True)
            If True, display state that forked.

        Returns
        -------------------
        is_forked_list : list of True/False
            is_forked_list[0] : Is sente's piece forked?
            is_forked_list[1] : Is  gote's piece forked?
        '''
        is_forked_list = []
        sente_index, gote_index = self.get_piece_indexes(query_piece)

        options = [
            ['-',  1, sente_index],
            ['+', -1,  gote_index]
        ]

        # For sente and gote
        for option in options:
            is_forked = False

            enemys_pm = option[0]
            direction = option[1]
            index = option[2]

            # For each cell of query_piece
            for i, j in index:
                fork_candidates = []

                # For each act of query_piece
                for act in eval('{}_ACT'.format(query_piece)):
                    for move in act:
                        next_i = i + move[0]
                        next_j = j + move[1] * direction

                        # If next_i or next_j is outside of the board
                        if (next_i < 0 or 9 <= next_i or
                                next_j < 0 or 9 <= next_j):
                            break

                        # If conflict with other piece
                        if self.board[next_i][next_j] != EMPTY_STR:
                            b = self.board[next_i][next_j]

                            if b[0] == enemys_pm:
                                fork_candidates.append(b[1])

                            break

                # If all targets in fork_candidates,
                #  print board & info.
                for target in targets:
                    if not target in fork_candidates:
                        break
                else:
                    if display:
                        self.plot_state_mpl()
                        print('forked by', enemys_pm, query_piece,
                              ':', ','.join(fork_candidates))

                    is_forked = True

            is_forked_list.append(is_forked)

        return is_forked_list
