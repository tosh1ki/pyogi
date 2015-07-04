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

    n = 11
    save_dir = os.path.expanduser('~/data/shogi/threads/')
    filename = '{0:04d}.htm'.format(n)
    filepath = os.path.join(save_dir, filename)

    with open(filepath, 'r') as f:
        html = f.read()

    html = re.sub('\n', '', html)

    REGEX_KAKI = ('<A\s+id=id_tag(\d+)\s+name=tag\d+>(.+?)'
                  '(?=(?:<A\s+id=id_tag\d+\s+name=tag\d+>)|</DL>)')
    kakikomi_list = re.findall(REGEX_KAKI, html, re.S|re.I)
    len(kakikomi_list)
