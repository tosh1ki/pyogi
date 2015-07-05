#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import pandas as pd
import pdb
sys.path.append('./../../')

from pyogi.ki2converter import *
from pyogi.kifu import *
from get_ki2_list import get_ki2_list


if __name__ == '__main__':

    path_ki2_list = get_ki2_list(argparse.ArgumentParser())
    kifu_table_list = []
    
    for path_ki2 in path_ki2_list:
            
        ki2converter = Ki2converter()
        ki2converter.from_path(path_ki2)

        csa = ki2converter.to_csa()

        if not csa:
            print('Cannot convert:', path_ki2)
            continue

        kifu = Kifu(csa)
        
        if not kifu.extracted:
            print('Cannot extract:', path_ki2)
            continue

        kifu_table = {
            'player0': kifu.players[0],
            'player1': kifu.players[1],
            'sente_win': kifu.sente_win,
            'sennnichite': kifu.is_sennichite,
            'joshogi': kifu.is_jishogi,
            'datetime': kifu.datetime,
            'teai': kifu.teai,
            'moves': ' '.join(kifu.moves),
            'description': kifu.description
        }
        kifu_table_list.append(kifu_table)

        if len(kifu_table_list) % 1000 == 0:
            print(len(kifu_table_list), flush=True)


    df = pd.DataFrame(kifu_table_list)
    df.to_csv('2chkifuzip_dataframe.csv')

    print(
        df
        .query('player0 == "谷川浩司"')
        .assign(first3=df.moves.str[0:8*3])
        .assign(count=1)
        .pipe(pd.pivot_table, 'count', 'first3', 'sente_win', aggfunc=sum)
    ) 
