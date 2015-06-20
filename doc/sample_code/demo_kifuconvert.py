#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('./../../')

from pyogi.ki2converter import *

if __name__ == '__main__':
    
    for n in range(2,100):
        if n in [4, 23, 29]:
            continue

        relpath = '~/data/shogi/2chkifu/00001/{:0>5}.KI2'.format(n)
        kifile = os.path.expanduser(relpath)
        
        ki2converter = Ki2converter()
        ki2converter.from_path(kifile)
        ki2converter.to_csa()
