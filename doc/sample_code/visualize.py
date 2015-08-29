#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

from pyogi.kifu import Kifu


if __name__ == '__main__':

    kifu = Kifu()

    df = pd.read_csv('2chkifuzip_dataframe.csv', index_col=0)

    player_list = []
    feature_list = []

    for index, d in df.iterrows():

        kifu.moves = d.moves.split(' ')
        kifu.players = [d.player0, d.player1]
        kifu.teai = d.teai
        kifu.reset_board()

        feature_list.append(kifu.make_features())
        player_list.append(d.player0)

        if index >= 1000:
            print(index, flush=True)
            break


    X = np.array(feature_list)
    y = np.array(player_list)

    X_unique = []
    players_unique2 = []

    players_unique = list(set(player_list))
    for player in players_unique:
        index = y == player
        if index.sum() <= 10:
            continue

        x = X[index, :].sum(axis=0)
        X_unique.append(x)
        players_unique2.append(player)

    # l2-normalize
    X_unique = np.array(X_unique)
    row_sums = np.sqrt((X_unique**2).sum(axis=1))
    X_unique = X_unique/row_sums[:, np.newaxis]

    plt.figure(figsize=(6, 17*len(players_unique2)/100))
    linkage = hierarchy.linkage(X_unique, method='ward')
    hierarchy.dendrogram(linkage, labels=players_unique2, orientation='right')
    plt.show()


    # Visualize using heatmap of board
    Y = X_unique[players_unique2.index('羽生善治'), 0:81]
    Y.shape = (9, 9)

    plt.pcolor(Y.T)
    plt.xlim(9, 0)
    plt.ylim(9, 0)
    plt.colorbar()
    plt.show()
