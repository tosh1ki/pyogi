#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
sys.path.append('./../../')

from pyogi.ki2converter import *


if __name__ == '__main__':

    # Convert kifu        
    for n in range(0, 50):
    
        path = ('~/data/shogi/2chkifu/{0}000{1}/{2:0>5}.KI2'
                .format(n // 10000, int(n < 10000), n))
        path_ki2 = os.path.expanduser(path)

        if not os.path.exists(path_ki2):
            continue

        ki2converter = Ki2converter()
        ki2converter.from_path(path_ki2)
        
        csa = ki2converter.to_csa()
