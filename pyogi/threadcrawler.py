#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import time
import requests


_REGEX_HTML = ('<dt>(\d+) ：([^：]+)：'
              '(\d+)/(\d+)/(\d+)\((.)\) (\d+):(\d+):([\d\.]+) '
              'ID:([\w\+/]+)(?:(?:.(?!=<dd>))+.)?<dd> (.+)')
_REGEX_HTML2 = ('<dt (?:id=res0_\d+)?><[^>]+?>'
                '<FONT color=black>(\d+)</FONT></A> ：([^：]+)：'
                '(\d+)/(\d+)/(\d+)\((.)\) (\d+):(\d+):([\d\.]+) '
                'ID:([\w\+/]+)(?:(?:.(?!=<dd>))+.)?<dd> (.+)')
REGEX_HTML = re.compile(_REGEX_HTML2, re.I)

def extract_kifutxt(html):
    return re.findall(REGEX_HTML, html)


class ThreadCrawler:

    def __init__(self, INTERVAL_TIME=3, MAX_N_RETRY=10):
        self.res = None
        self.html = None
        self.INTERVAL_TIME = INTERVAL_TIME
        self.MAX_N_RETRY = MAX_N_RETRY

    def get_response(self, url):
        '''指定したurlのhtmlを取得する
        '''
        time.sleep(self.INTERVAL_TIME)

        for n in range(self.MAX_N_RETRY):
            time.sleep(10 * n * self.INTERVAL_TIME)

            try:
                res = requests.get(url)

            except requests.ConnectionError:
                print('\nConnection aborted.\n')
                res = None

            if res and res.status_code == 200:
                self.res = res
                self.html = self.res.content.decode('CP932')

                break
            else:
                print('\nretry (ThreadCrawler.get_response())\n')
                sys.stdout.flush()
        else:
            sys.exit('Exceeded MAX_N_RETRY (WarsCrawler.get_html())')

    def extract_kifutxt(self):
        return extract_kifutxt(self.html)

    def save_html(self, savepath):
        with open(savepath, 'w') as f:
            f.write(self.html)
