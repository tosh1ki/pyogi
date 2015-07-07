#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append('./../../')

from pyogi.board import Board, EMPTY_STR


if __name__ == '__main__':

    board = Board()
    sum_list = [[[] for _ in range(9)] for _ in range(9)]
    count_list = [[None for _ in range(9)] for _ in range(9)]

    df = pd.read_csv('2chkifuzip_dataframe.csv', index_col=0)
    df_habu_sente = df.query('player0 == "羽生善治"')

    for index, d in df_habu_sente.iterrows():

        board.set_initial_state()

        for move_csa in d.moves.split(' '):
            board.move(move_csa)

            for i in range(9):
                for j in range(9):
                    grid = board.board[i][j]
                    
                    if grid == EMPTY_STR or grid[0] == '-':
                        continue

                    sum_list[i][j].append(grid[1])

                
    for i in range(9):
        for j in range(9):
            count_list[i][j] = sum_list[i][j].count('OU')

    plt.pcolor(np.array(count_list).T)
    plt.xlim(9, 0)
    plt.ylim(9, 0)
    plt.colorbar()
