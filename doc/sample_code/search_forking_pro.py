#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    
        relpath = '~/data/shogi/2chkifu/{0}000{1}/{2:0>5}.KI2'.format(n1, n2, n)
        kifile = os.path.expanduser(relpath)

        if not os.path.exists(kifile):
            continue
            
        ki2converter = Ki2converter()
        ki2converter.from_path(kifile)

        csa = ki2converter.to_csa()

        if not csa:
            continue

        kifu = Kifu(csa)
        res = kifu.get_forking(['OU', 'HI'])
        if res[2] or res[3]:
            print(kifu.players)

        # Output
        # 1. sente forked | gote forked
        # 2. (sente won & sente forked) | (gote won & gote forked)
        res_table.append(
            [n,
             kifu.players[0],
             kifu.players[1],
             kifu.sente_win,
             kifu.is_sennichite,
             res[2] != [],
             res[3] != [],
             res[2] != [] or res[3] != [],
             (kifu.sente_win and res[2]!=[]) or 
             ((not kifu.sente_win) and res[3]!=[])])


        break

    columns = ['n', 'player0', 'player1', 'sente_win',
               'sennichite', 'sente_forking', 'gote_forking',
               'fork', 'fork&win']
    df = pd.DataFrame(res_table, columns=columns)

    pd.crosstab(df.loc[:, 'fork'], df.loc[:, 'fork&win'])
