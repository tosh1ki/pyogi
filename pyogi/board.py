#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pdb

from .pieces_act import *

empty_str = '   '
all_mochigoma = ['FU']*9 + ['KI', 'GI', 'KE', 'KY']*2 + ['HI', 'KA', 'OU']
board_indexes = list(range(0, 9))
SENTE = '+'
GOTE = '-'

class Board:
    '''Shogi board class

    Member variables
    -------------------
    Board.board : list (two-dimensional array, 9 x 9)
        If you want to move a piece as '☗7六歩',
        >>> board[6][5] = ['+', 'FU']
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
        self.board = [[empty_str]*9 for n in range(9)]
        self.mochigoma = [[], []]
        self.tesu = 0
        self.last_move = ''

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        row_separator = '-'*37

        sente_mochigoma = ','.join(self.mochigoma[0])
        gote_mochigoma = ','.join(self.mochigoma[1])
        s = ['{}手目: {}'.format(self.tesu, self.last_move),
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

    def __setitem__(self, index, value):
        self.board[index] = value

    def __getitem__(self, index):
        return self.board[index]

    def set_initial_state(self):
        '''Set state as hirate initial state.
        '''
        self.mochigoma = [list(all_mochigoma), list(all_mochigoma)]

        curdir = os.path.dirname(__file__)
        csapath = os.path.join(curdir, 'initial_state.csa')
        with open(csapath, 'r') as f:
            initial_csa = f.read()

        moves = initial_csa.split('\n')

        for move in moves:
            if move:
                self.move(move)

        self.last_move = ''
        self.tesu = 0

    def move(self, move):
        '''Move a piece on a board

        Args
        -------------------
        move : str
            Move CSA format
            ex. '+9998KY'
        '''
        teban = int(move[0] != '+')  ## 0 if sente, 1 if gote

        points = list(map(int, list(move[1:5])))
        prev_point = points[0:2]
        next_point = points[2:4]
        koma = move[5:]

        if prev_point == [0, 0]:
            # use mochigoma
            self.mochigoma[teban].remove(koma)
        else:
            self.board[prev_point[0] - 1][prev_point[1] - 1] = empty_str

        next_point_info = self.board[next_point[0] - 1][next_point[1] - 1]
        if next_point_info != empty_str:
            # pick enemy's koma
            picked_koma = next_point_info[1]

            # なった駒を取る場合
            if picked_koma in TURN_PIECE:
                picked_koma = TURN_PIECE[picked_koma]

            self.mochigoma[teban].append(picked_koma)

        self.board[next_point[0] - 1][next_point[1] - 1] = [move[0], koma]
        
        self.last_move = move
        self.tesu += 1

    def get_piece_indexes(self, piece):
        '''Get indexes of piece on a board.

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
        sente_index = []
        gote_index = []

        for j, column in enumerate(self.board):
            for i, value in enumerate(column):
                teban = value[0]
                board_piece = value[1]
                if board_piece == piece:
                    if teban == SENTE:
                        sente_index.append([j, i])
                    elif teban == GOTE:
                        gote_index.append([j, i])

        return [sente_index, gote_index]

    def is_forking(self, targets = ['OU', 'HI'], display = True):
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

    def is_forking_query(self, query_piece, targets, display = True):
        '''Check that there is an piece which forked by enemy's piece.
        Search a state that `query_piece` forks all pieces of `target` at.

        Args
        -------------------
        query_piece : str
            ex. 'KA'
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
        is_forked_list = []
        sente_index, gote_index = self.get_piece_indexes(query_piece)

        options = [
            ['-',  1, sente_index],
            ['+', -1,  gote_index]
        ]

        ## pdb.set_trace()

        ## for sente and gote
        for option in options:
            is_forked = False

            enemys_pm = option[0]
            direction = option[1]
            index = option[2]

            ## for each cell of query_piece
            for i, j in index:
                fork_candidates = []

                ## for each act(効き) of query_piece
                for act in eval('{}_ACT'.format(query_piece)):
                    for move in act:
                        next_i = i + move[0]
                        next_j = j + move[1] * direction

                        ## if next_i or next_j is outside of the board
                        if (next_i < 0 or 9 <= next_i or
                            next_j < 0 or 9 <= next_j):
                            break

                        #print(next_i, next_j, self.board[next_i][next_j])
                    
                        ## if conflict with other piece
                        if self.board[next_i][next_j] != empty_str:
                            b = self.board[next_i][next_j]
                        
                            if b[0] == enemys_pm:
                                fork_candidates.append(b[1])
                            
                            break

                ## if all targets in fork_candidates,
                ## print board & info.
                for target in targets:
                    if not target in fork_candidates:
                        break
                else:
                    if display:
                        print(self)
                        print('forked by', enemys_pm, query_piece,
                              ':', ','.join(fork_candidates))

                    is_forked = True


            is_forked_list.append(is_forked)

        return is_forked_list
