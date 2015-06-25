#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
駒落ちの棋譜を10枚集めてそのうち適当に1つを表示
'''

import os
import sys
import argparse
sys.path.append('./../../')

from pyogi.ki2converter import *
from get_ki2_list import get_ki2_list


if __name__ == '__main__':

    path_ki2_list = get_ki2_list(argparse.ArgumentParser())
    path_komaochi = []
    
    for path_ki2 in path_ki2_list:
        ki2converter = Ki2converter()
        ki2converter.from_path(path_ki2)
        
        if '下手' in ki2converter.ki2_txt and '上手' in ki2converter.ki2_txt:
            path_komaochi.append(path_ki2)
            if len(path_komaochi) > 10:
                break

    path_ki2 = path_komaochi[2]

    ki2converter = Ki2converter()
    ki2converter.from_path(path_ki2)

    csa = ki2converter.to_csa()
    print(csa)
    print(ki2converter.board)
