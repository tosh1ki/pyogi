import os
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
font = {'family': 'TakaoGothic'}
matplotlib.rc('font', **font)

from .pieces_act import KOMA_INFOS, KOMAOCHI_OPTIONS, PIECE_TO_ACT

import pdb

row_separator = '-' * 37
board_indexes = list(range(0, 9))

all_mochigoma_csa = (['FU'] * 9 + ['KI', 'GI', 'KE', 'KY'] * 2
                     + ['HI', 'KA', 'OU'])
all_mochigoma = list(map(Koma, all_mochigoma_csa))

initial_state_csa = '''
+0017FU
+0027FU
+0037FU
+0047FU
+0057FU
+0067FU
+0077FU
+0087FU
+0097FU
+0019KY
+0029KE
+0039GI
+0049KI
+0059OU
+0069KI
+0079GI
+0089KE
+0099KY
+0028HI
+0088KA
-0013FU
-0023FU
-0033FU
-0043FU
-0053FU
-0063FU
-0073FU
-0083FU
-0093FU
-0011KY
-0021KE
-0031GI
-0041KI
-0051OU
-0061KI
-0071GI
-0081KE
-0091KY
-0082HI
-0022KA
'''


cdef class Board:

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
        self.board = [[''] * 9 for _ in range(9)]
        self.mochigoma = []
        self.tesu = 0
        self.last_move_txt = ''
        self.last_move_xy = []
        self.teai = ''
        self.players = ['', '']

    def __str__(self):
        sente_mochigoma = self.get_mochigoma_str(0, kanji=False)
        gote_mochigoma = self.get_mochigoma_str(1, kanji=False)

        s = ['{}手目: {}'.format(self.tesu, self.last_move_txt),
             gote_mochigoma, row_separator]

        for j in board_indexes:
            s_j = [self.board[i][j].__str__() for i in board_indexes[::-1]]
            s_temp = '|' + '|'.join(s_j) + '|'
            s.append(s_temp)
            s.append(row_separator)

        s.append(sente_mochigoma)  # sente's mochigoma

        return '\n'.join(s)

    def __setitem__(self, index, value):
        self.board[index] = value

    def __getitem__(self, index):
        return self.board[index]

    def plot_state_mpl(self, figsize=(8, 9), title = '', savepath=''):
        '''Plot current state using matplotlib.

        Args
        -------------------
        figsize : tuple of int, optional (default = (8, 9))
            Figure size of output
        title : str, optional (default = '')
            If title == '', plot a string of last move.
        savepath : str, optional (default = '')
            If savepath != None, save output of matplotlib as a png file
        '''
        fig, ax = plt.subplots(figsize=figsize)

        width_x = figsize[0]
        width_y = figsize[1]

        plt.xlim(0, width_x)
        plt.ylim(0, width_y)

        dx = width_x / 9
        dy = width_y / 9

        fontsize = 30 * min(dx, dy)

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
                grid = self.board[b_i][j]

                x = ((8 - i) + 1 / 2) * dx
                y = ((8 - j) + 1 / 2) * dy

                if not grid.is_empty():
                    is_gote = not grid.is_of_sente()
                    # TOFIX: 60, 80にするとよくわからないけどうまくいく
                    plt.text(x - fontsize / 2 / 60, y - fontsize / 2 / 80,
                             grid.koma.kanji,
                             size=fontsize, rotation=180 * is_gote)

                # Plot circle around piece moved recently
                if (len(self.last_move_xy) == 2 and
                        self.last_move_xy[0] == i and
                        self.last_move_xy[1] == j):
                    circle = Circle((x, y), 0.5 * dx, facecolor='none',
                                    linewidth=3, alpha=0.5)
                    ax.add_patch(circle)

        # Plot mochigoma
        plt.text(0, -0.5 * dx, self.get_mochigoma_str(0),
                 fontsize=fontsize)
        plt.text(0,  9.2 * dy, self.get_mochigoma_str(1),
                 fontsize=fontsize, rotation=180)

        # Plot names
        plt.text(width_x + 0.2, 2 * dy, self.players[0],
                 fontsize=fontsize, rotation=90)
        plt.text(width_x + 0.2, 8 * dy, self.players[1],
                 fontsize=fontsize, rotation=90)

        # Plot title
        if not title:
            title = '{0}手目: {1}'.format(self.tesu, self.last_move_txt)

        plt.title(title, y=1.07, fontsize=fontsize)
        plt.tick_params(labelleft='off', labelbottom='off')

        if savepath:
            fig.savefig(savepath)
        else:
            plt.show()

    cpdef str get_mochigoma_str(self, int teban, bool_t kanji=True):
        '''Returns string of all mochigoma.

        teban : int
            0 : sente
            1 : gote
        '''
        cdef:
            Koma k, m

        if kanji:
            mochigoma = [m.kanji for m in self.mochigoma[teban]]
            koma = list(KOMA_INFOS.kanji)
        else:
            mochigoma = [m.csa for m in self.mochigoma[teban]]
            koma = list(KOMA_INFOS.csa)

        counter = Counter(mochigoma)
        mochigoma_list = []

        for k in koma:
            if counter[k] == 1:
                mochigoma_list.append(k)
            elif counter[k] > 1:
                mochigoma_list.append('{0}x{1}'.format(k, counter[k]))

        return ' '.join(mochigoma_list)

    cpdef int set_initial_state(self, str teai='hirate'):
        '''Set state as initial state (with handicap).

        Args
        -------------------
        teai : str, optional (default = 'hirate')
            Type of komaoti (handicap)
            ex. hirate, kakuoti, hisyaoti, kyouoti,migikyouoti,
                hikyouoti, nimaioti, sanmaioti, yonmaioti, rokumaioti
        '''
        cdef:
            int n, i, j
            str move, p, dp
            list moves

        self.board = [[Grid()] * 9 for n in range(9)]
        self.mochigoma = [list(all_mochigoma), list(all_mochigoma)]

        moves = initial_state_csa.split('\n')

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

            if self.board[i][j].which_player == '-' and self.board[i][j].koma.csa == p:
                self.board[i][j].reset()

        self.last_move_txt = ''
        self.last_move_xy = []
        self.tesu = 0
        self.teai = teai

    cpdef list move(self, str move):
        '''Move a piece on a board

        Args
        -------------------
        move : str
            Move CSA format
            ex. '+9998KY'
        '''
        cdef:
            int teban
            list points, prev_point, next_point
            str koma, picked_koma_csa = ''
            Koma m, picked_koma
            Grid prev_grid, next_grid, next_grid_new

        teban = int(move[0] != '+')  # 0 if sente, 1 if gote

        points = list(map(int, list(move[1:5])))
        prev_point = points[0:2]
        next_point = points[2:4]
        koma = move[5:]

        if prev_point == [0, 0]:
            # use mochigoma
            for m in self.mochigoma[teban]:
                if m.csa == koma:
                    self.mochigoma[teban].remove(m)
                    break
            prev_koma = koma
        else:
            prev_grid = self.board[prev_point[0] - 1][prev_point[1] - 1]

            if prev_grid.koma.csa_rear == koma:
                prev_grid.koma.promote()

            prev_koma = prev_grid.koma.csa
            self.board[prev_point[0] - 1][prev_point[1] - 1].reset()

        next_grid = self.board[next_point[0] - 1][next_point[1] - 1]

        # If picking enemy's koma
        if not next_grid.is_empty():
            picked_koma = next_grid.koma

            # If picking promoted piece
            if picked_koma and picked_koma.is_promoted:
                picked_koma.depromote()

            self.mochigoma[teban].append(picked_koma)
            picked_koma_csa = picked_koma.csa

        next_grid_new = Grid(move[0], prev_koma)
        self.board[next_point[0] - 1][next_point[1] - 1] = next_grid_new

        self.last_move_txt = move
        self.last_move_xy = [next_point[0] - 1, next_point[1] - 1]
        self.tesu += 1

        return [next_grid_new.koma.csa, picked_koma_csa]

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
        cdef:
            int i, j
            str teban
            list column
            Grid grid
            list pieces_index

        pieces_index = [[], []]
        for j, column in enumerate(self.board):
            for i, grid in enumerate(column):
                teban = grid.which_player

                if grid.koma and grid.koma.csa == piece:
                    pieces_index[teban == '-'].append([j, i])

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
        cdef str query_piece

        results = [False, False]

        for query_piece in list(KOMA_INFOS.csa):
            results_tmp = self.is_forking_query(query_piece, targets, display)
            results = [results[0] or results_tmp[0],
                       results[1] or results_tmp[1]]

        return results

    cpdef list is_forking_query(self, str query_piece, list targets, bool_t display=True):
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
        cdef:
            list is_forked_list = [], fork_candidates
            list sente_index, gote_index, options, option
            str enemys_pm, target
            int direction, i, j, next_i, next_j
            list index, act, move
            bool_t is_forked

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
                for act in PIECE_TO_ACT[query_piece]:
                    for move in act:
                        next_i = i + move[0] * direction
                        next_j = j + move[1] * direction

                        # If next_i or next_j is outside of the board
                        if (next_i < 0 or 9 <= next_i or
                                next_j < 0 or 9 <= next_j):
                            break

                        # If conflict with other piece
                        if not self.board[next_i][next_j].is_empty():
                            grid = self.board[next_i][next_j]

                            if grid.which_player == enemys_pm:
                                fork_candidates.append(grid.koma.csa)

                            break

                # If all targets in fork_candidates,
                #  print board & info.
                for target in targets:
                    if target not in fork_candidates:
                        break
                else:
                    if display:
                        self.plot_state_mpl()
                        print('forked by', enemys_pm, query_piece,
                              ':', ','.join(fork_candidates))

                    is_forked = True

            is_forked_list.append(is_forked)

        return is_forked_list
