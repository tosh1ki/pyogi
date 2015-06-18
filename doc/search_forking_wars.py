#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This script finds states that OU and HI are forked at,
using data that crawled by shogiwars.
'''

import os
import sys
sys.path.append('./../')
import sqlite3
import pandas as pd

from pyogi.kifu import *


if __name__ == '__main__':

    dbpath = os.path.expanduser('~/data/sqlite3/shogiwars.sqlite3')
    con = sqlite3.connect(dbpath)

    query = 'SELECT * FROM kifu LIMIT 100;'
    df = pd.read_sql(query, con).drop_duplicates()

    for key, d in df.T.to_dict().items():
        kifu = Kifu(d['csa'])

        if kifu.extracted:
            results = kifu.get_forking(['OU', 'HI'])

            if results[0] != [] or results[1] != []:
                print(d['name'])
                print()
