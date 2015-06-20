#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('./../../')

from pyogi.ki2converter import *

if __name__ == '__main__':
    
    for n in range(0, 50000):

        n1 = (n // 10000)
        n2 = int(n < 10000)
    
        relpath = '~/data/shogi/2chkifu/{0}000{1}/{2:0>5}.KI2'.format(n1, n2, n)
        kifile = os.path.expanduser(relpath)

        if not os.path.exists(kifile):
            continue
            
        ki2converter = Ki2converter()
        ki2converter.from_path(kifile)

        ki2converter.to_csa()
