#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
2chの「将棋の棋譜貼り専門スレッド」から棋譜を収集するデモ
'''

import sys
sys.path.append('./../../')

from pyogi.kifu import Kifu
from pyogi.threadcrawler import ThreadCrawler
from pyogi.ki2converter import Ki2converter


if __name__ == '__main__':

    # Crawl html that contains kifu of KI2 format
    # From "将棋の棋譜貼り専門スレッド Part121 [転載禁止]©2ch.net"
    url = 'http://peace.2ch.net/test/read.cgi/bgame/1428330063/'
    crawler = ThreadCrawler()
    crawler.get_response(url)
    matched = crawler.extract_kifutxt()

    # Extract one of kifu text
    ki2 = [m[10] for m in matched  if '▲' in m[10] and '△' in m[10]]
    ki2txt = re.sub(' (?:<br> )+', '\n', ki2[0])

    # Convert the kifu from KI2 to CSA
    ki2converter = Ki2converter()
    ki2converter.from_txt(ki2txt)
    csa = ki2converter.to_csa()

    # Print last state
    kifu = Kifu(csa)
    kifu.print_state(mode='mpl')
