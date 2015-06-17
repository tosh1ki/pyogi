#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb

empty_str = '   '
all_mochigoma = ['FU']*9 + ['KI', 'GI', 'KE', 'KY']*2 + ['HI', 'KA', 'OU']
board_indexes = list(range(0, 9))
turn_koma = {
    'TO': 'FU', 'NY': 'KY', 'NK': 'KE',
    'NG': 'GI', 'UM': 'KA', 'RY': 'HI'
}

class Board:
    '''Shogi board class

    Member variables
    -------------------
    Board.board : list (two-dimensional array, 9 x 9)
        If you want to move a piece as '☗7六歩'
        >>> board[6][5] = ['+', 'FU']
    Board.mochigoma : list
        mochigoma list

    Examples
    -------------------
    >>> board = Board()
    >>> board.set_initial_state()
    >>> board.move('+7776FU')
    '''
    def __init__(self):
        self.board = [[empty_str]*9 for n in range(9)]
        self.mochigoma = [[], []]
        self.tesu = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        row_separator = '-'*37

        sente_mochigoma = ','.join(self.mochigoma[0])
        gote_mochigoma = ','.join(self.mochigoma[1])
        s = ['{}手目'.format(self.tesu), gote_mochigoma, row_separator]

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

        with open('initial_state.csa', 'r') as f:
            initial_csa = f.read()

        moves = initial_csa.split('\n')

        for move in moves:
            if move:
                self.move(move)

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

        prev_point_info = board[prev_point[0] - 1][prev_point[1] - 1]
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
            if picked_koma in turn_koma:
                picked_koma = turn_koma[picked_koma]

            self.mochigoma[teban].append(picked_koma)

        self.board[next_point[0] - 1][next_point[1] - 1] = [move[0], koma]
        
        self.tesu += 1

if __name__ == '__main__':
    board = Board()
    board.set_initial_state()
    board.move('+7776FU')
    board.move('-3334FU')
    board.move('+8822UM')
    board.move('-3122GI')
    print(board)
