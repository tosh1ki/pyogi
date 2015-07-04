#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
sys.path.append('./../../../')

from pyogi.kifu import Kifu
from pyogi.threadcrawler import extract_kifutxt
from pyogi.ki2converter import Ki2converter


if __name__ == '__main__':

    save_dir = os.path.expanduser('~/data/shogi/threads/')
    file_list = os.listdir(save_dir)

    for filename in sorted(file_list):
        filepath = os.path.join(save_dir, filename)
    
        with open(filepath, 'r') as f:
            html = f.read()

        html = re.sub('\n', '', html)

        kakikomi_list = extract_kifutxt(html)
        print(filename, len(kakikomi_list))

        break


    kifu_list = []
    for kakikomi in kakikomi_list:
        txt = re.sub('<BR>', '\n', kakikomi)
        txt = re.sub('^.+?<DD[^>]+?>', '', txt)
        txt = re.sub('<A[^>]+?>', '', txt)
        
        converter = Ki2converter()
        converter.from_txt(txt)

        if not converter.moves_ki2:
            continue

        try:
            csa = converter.to_csa()
        except (KeyError, AttributeError, ValueError):
            continue

        if csa:
            kifu = Kifu(csa)
            kifu.print_state(mode='mpl')

            kifu_list.append(kifu)
