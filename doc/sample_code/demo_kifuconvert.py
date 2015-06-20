#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('./../../')

from pyogi.ki2converter import *

if __name__ == '__main__':
    
    for n in range(10000, 20000):

        if n in [1]:
            continue

        relpath = '~/data/shogi/2chkifu/10000/{:0>5}.KI2'.format(n)
        kifile = os.path.expanduser(relpath)

        if not os.path.exists(kifile):
            continue
        
        ki2converter = Ki2converter()
        ki2converter.from_path(kifile)

        ki2converter.to_csa()

        # try:
        #     ki2converter.to_csa()
        # except RuntimeError:
        #     print('RuntimeError')
