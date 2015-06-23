#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
プロ棋士の棋譜の中から王手飛車取りの場面を探して，
「プロの対局では王手飛車をかけたほうが負ける」が本当かどうかを確かめる
'''

import os
import sys
import pandas as pd
sys.path.append('./../../')

from pyogi.ki2converter import *
from pyogi.kifu import *


if __name__ == '__main__':

    res_table = []
    
    for n in range(0, 50000):

        n1 = (n // 10000)
        n2 = int(n < 10000)
    
        path = '~/data/shogi/2chkifu/{0}000{1}/{2:0>5}.KI2'.format(n1, n2, n)
        kifile = os.path.expanduser(path)

        if not os.path.exists(kifile):
            continue
            
        ki2converter = Ki2converter()
        ki2converter.from_path(kifile)

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
                'n': n,
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
