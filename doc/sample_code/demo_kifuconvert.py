#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
sys.path.append('./../../')

from pyogi.ki2converter import *
from get_ki2_list import get_ki2_list


if __name__ == '__main__':

    path_ki2_list = get_ki2_list(argparse.ArgumentParser())

    # Convert kifu
    for path_ki2 in path_ki2_list:
        ki2converter = Ki2converter()
        ki2converter.from_path(path_ki2)
        
        csa = ki2converter.to_csa()
        print(csa)
        print(ki2converter.board)
        print()
