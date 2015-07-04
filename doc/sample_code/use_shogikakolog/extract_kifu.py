#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import pandas as pd
sys.path.append('./../../../')

from pyogi.kifu import Kifu
from pyogi.threadcrawler import extract_kakikomitxt
from pyogi.ki2converter import Ki2converter

import pdb


if __name__ == '__main__':

    save_dir = os.path.expanduser('~/data/shogi/threads/')
    file_list = os.listdir(save_dir)
    kakikomi_list = []

    for filename in sorted(file_list, reverse=True)[2:]:
        filepath = os.path.join(save_dir, filename)
    
        with open(filepath, 'r') as f:
            html = f.read()

        html = re.sub('\n', '', html)

        kakikomis = extract_kakikomitxt(html)
        kakikomi_list.extend(kakikomis)
        print(filename, len(kakikomis))


    kifu_list = []
    kifu_infos_list = []

    for kakikomi in kakikomi_list:

        txt = re.sub('<br> ', '\n', kakikomi)
        txt = re.sub('^.+?<DD[^>]+?>', '', txt)
        txt = re.sub('<A[^>]+?>', '', txt)
        txt = re.search('(開始日時：.+?手で(?:[先後]手の勝ち|千日手))', txt, re.S)
        # Future works:
        #  Implement case for long kifu 

        # If there is NOT strings of kifu like KI2 format
        if not txt:
            continue
        else:
            txt = txt.group()

        converter = Ki2converter()
        converter.from_txt(txt)

        # If converter cannot extract moves of KI2 format
        if not converter.moves_ki2:
            continue

        try:
            csa = converter.to_csa()
        except UnicodeDecodeError:
            print(kakikomi)
            continue

        # If extracted kifu of CSA format
        if csa:
            kifu = Kifu(csa)
            kifu_list.append(kifu)
        else:
            print(txt)

        n_kifu = len(kifu_list)
        if n_kifu%1000 == 0:
            print(n_kifu)


        kifu_table = {
            'player0': kifu.players[0],
            'player1': kifu.players[1],
            'sente_win': kifu.sente_win,
            'datetime': kifu.datetime,
            'teai': kifu.teai,
            'moves': ' '.join(kifu.moves),
            'description': kifu.description
        }

        kifu_infos_list.append(kifu_table)


    df = pd.DataFrame(kifu_infos_list)
    csvpath = os.path.expanduser('~/data/shogi/output/thread_kifu.csv')
    df.to_csv(csvpath)
