#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This script finds states that OU and HI are forked at,
using data that crawled by shogiwars.
'''

import os
import sys
sys.path.append('./../../')
import sqlite3
import pandas as pd

from pyogi.kifu import *


if __name__ == '__main__':

    dbpath = os.path.expanduser('~/data/sqlite3/shogiwars.sqlite3')
    con = sqlite3.connect(dbpath)

    query = 'SELECT * FROM kifu LIMIT 100;'
    df = pd.read_sql(query, con).drop_duplicates().reset_index()

    res_table = []

    for key, d in df.T.to_dict().items():
        kifu = Kifu(d['csa'])

        if not kifu.extracted:
            continue

        res = kifu.get_forking(['OU', 'HI'])

        if res[2] or res[3]:
            print(kifu.players)

        # Data
        #   fork: sente forked | gote forked
        #   forkandwin: (sente won & sente forked) | (gote won & gote forked)
        res_table.append(
            {
                'id': d['name'],
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
    df_ct = pd.DataFrame(res_table)
    print(pd.crosstab(df_ct.loc[:, 'fork'], df_ct.loc[:, 'forkandwin']))
