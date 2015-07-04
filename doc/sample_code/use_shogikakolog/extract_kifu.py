#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
sys.path.append('./../../../')

from pyogi.kifu import Kifu
from pyogi.threadcrawler import extract_kifutxt
from pyogi.ki2converter import Ki2converter

import pdb


if __name__ == '__main__':

    save_dir = os.path.expanduser('~/data/shogi/threads/')
    file_list = os.listdir(save_dir)
    kakikomi_list = []

    for filename in sorted(file_list, reverse=True):
        filepath = os.path.join(save_dir, filename)
    
        with open(filepath, 'r') as f:
            html = f.read()

        html = re.sub('\n', '', html)

        kakikomis = extract_kifutxt(html)
        kakikomi_list.extend(kakikomis)
        print(filename, len(kakikomis))

        break


    kifu_list = []
    for kakikomi in kakikomi_list:
        txt = re.sub('<br> ', '\n', kakikomi)
        txt = re.sub('^.+?<DD[^>]+?>', '', txt)
        txt = re.sub('<A[^>]+?>', '', txt)
        
        converter = Ki2converter()
        converter.from_txt(txt)

        if not converter.moves_ki2:
            continue

        try:
            csa = converter.to_csa()
        except UnicodeDecodeError:
            print(kakikomi)

            continue

        if csa:
            kifu = Kifu(csa)
            kifu_list.append(kifu)

        n_kifu = len(kifu_list)
        if n_kifu%1000 == 0:
            print(n_kifu)
