#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
sys.path.append('./../')

from pyogi.ki2converter import Ki2converter


if __name__ == '__main__':

    # Convert kifu        
    csa_list = []
    for n in range(0, 10):
    
        path = './../data/{0:0>5}.KI2'.format(n)
        path_ki2 = os.path.expanduser(path)

        if not os.path.exists(path_ki2):
            continue

        ki2converter = Ki2converter()
        ki2converter.from_path(path_ki2)
        
        csa = ki2converter.to_csa()

        csa_list.append(csa)

    print(csa_list)
