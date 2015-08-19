#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
WarsCrawlerのデモ
'''

import os
import sys
import argparse
sys.path.append('./../../')

from pyogi.warscrawler import WarsCrawler, gtype_dict


if __name__ == '__main__':

    dbpath = os.path.expanduser('./test.sqlite3')
    wcrawler = WarsCrawler(dbpath, interval=5, n_retry=10)
    csvpath = 'crawled.csv'
    tournament_name = 'tentei'

    # csvpathのファイルが存在しない場合
    if not os.path.exists(csvpath):
        for mode, gtype in gtype_dict.items():
            t_users = wcrawler.get_users(tournament_name, max_page=1)
            df_url = wcrawler.get_kifu_url(t_users[-2:], gtype, csvpath)

    df_kifu = wcrawler.get_all_kifu(csvpath)
