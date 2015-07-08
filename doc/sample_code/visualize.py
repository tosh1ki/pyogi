#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
sys.path.append('./../../')

from pyogi.kifu import Kifu


if __name__ == '__main__':

    kifu = Kifu()

    df = pd.read_csv('2chkifuzip_dataframe.csv', index_col=0)
    df = df.query('player0 == "羽生善治" or player0 == "森内俊之" or player0 == "藤井　猛"')
    df = df.iloc[0:100, :]

    player_list = []
    feature_list = []

    for index, d in df.iterrows():

        kifu.moves = d.moves.split(' ')
        kifu.players = [d.player0, d.player1]
        kifu.teai = d.teai
        kifu.reset_board()

        feature_list.append(kifu.make_features())
        player_list.append(d.player0)


    X = np.array(feature_list)

    plt.figure(figsize=(6, 17*len(player_list)/100))
    linkage = hierarchy.linkage(X)
    hierarchy.dendrogram(linkage, labels=player_list, orientation='right')
    plt.show()

    # Visualize using heatmap of board
    Y = X[0,:]
    Y.shape = (9, 9)

    plt.pcolor(Y.T)
    plt.xlim(9, 0)
    plt.ylim(9, 0)
    plt.colorbar()
    plt.show()

