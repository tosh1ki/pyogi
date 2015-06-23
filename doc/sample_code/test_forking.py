#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('./../../')

from pyogi.kifu import *

if __name__ == '__main__':

    kifu_path = './../../testgetfork.csa'
    with open(kifu_path, 'r') as f:
        kifu_txt = f.read()

    kifu = Kifu(kifu_txt)
    results = kifu.get_forking(['OU', 'HI'])
