#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('./../')
import sqlite3
import pandas as pd

from pyogi.kifu import *


if __name__ == '__main__':

    dbpath = os.path.expanduser('~/data/sqlite3/shogiwars.sqlite3')
    con = sqlite3.connect(dbpath)

    query = 'SELECT * FROM kifu LIMIT 1000;'
    df = pd.read_sql(query, con)

    for key, d in df.T.to_dict().items():
        kifu = Kifu(d['csa'])
        results = kifu.get_forking(['OU', 'HI'])

        if True in results:
            print(d['name'])

        print()
