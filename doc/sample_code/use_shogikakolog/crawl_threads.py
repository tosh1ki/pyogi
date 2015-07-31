#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import requests

sys.path.append('./../../../')

from pyogi.threadcrawler import ThreadCrawler


if __name__ == '__main__':

    url_base = 'http://shogikakolog.web.fc2.com/part{0:02d}.htm'
    save_dir = os.path.expanduser('~/data/shogi/threads/')

    n_max = 120

    for n in range(1, 120):
        if n == 72:
            continue

        url = url_base.format(n)
        filename = '{0:04d}.htm'.format(n)
        filepath = os.path.join(save_dir, filename)

        if not os.path.exists(filepath):
            crawler = ThreadCrawler()
            crawler.get_response(url)
            crawler.save_html(filepath)

        print(filepath)
            
