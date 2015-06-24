#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
プロ棋士の棋譜の中から王手飛車取りの場面を探して，
「プロの対局では王手飛車をかけたほうが負ける」が本当かどうかを確かめる

2chkifu.zipをダウンロードして適当なディレクトリに解凍，
`python3 search_forking_pro.py -p [2chkifuのパス]` のような感じで実行する
'''

import os
import sys
import argparse
import pandas as pd
sys.path.append('./../../')

from pyogi.ki2converter import *
from pyogi.kifu import *


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path_2chkifu',
                        default='~/data/shogi/2chkifu/',
                        help='2chkifu.zipを展開したディレクトリ')
    args = parser.parse_args()
    path_2chkifu = args.path_2chkifu

    sub_dir_list = ['00001', '10000', '20000', '30000', '40000']
    path_ki2_list = []

    # Extract paths of KI2 files
    for sub_dir in sub_dir_list:
        path_dir = os.path.expanduser(os.path.join(path_2chkifu, sub_dir))
        ki2files = os.listdir(path_dir)

        for ki2file in ki2files:
            path_ki2_list.append(os.path.join(path_dir, ki2file))


    res_table = []
    
    for path_ki2 in path_ki2_list:
            
        ki2converter = Ki2converter()
        ki2converter.from_path(path_ki2)

        csa = ki2converter.to_csa()

        if not csa:
            continue

        kifu = Kifu(csa)
        
        if not kifu.extracted:
            continue

        res = kifu.get_forking(['OU', 'HI'], display=False)
        if res[2] or res[3]:
            print(kifu.players)

        # Data
        #   fork: sente forked | gote forked
        #   forkandwin: (sente won & sente forked) | (gote won & gote forked)
        res_table.append(
            {
                'path': path_ki2,
                'player0': kifu.players[0],
                'player1': kifu.players[1],
                'sente_won': kifu.sente_win,
                'sennichite': kifu.is_sennichite,
                'sente_forking': res[2] != [],
                'gote_forking': res[3] != [],
                'fork': res[2] != [] or res[3] != [],
                'forkandwin': ((kifu.sente_win and res[2]!=[]) or 
                               (not kifu.sente_win and res[3]!=[]))
            }
        )


    # Output
    df = pd.DataFrame(res_table)
    print(pd.crosstab(df.loc[:, 'fork'], df.loc[:, 'forkandwin']))
