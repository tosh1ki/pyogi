#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import time
import requests


_REGEX_HTML2 = ('<A\s+id=id_tag(\d+)\s+name=tag\d+>(.+?)'
                '(?=(?:<A\s+id=id_tag\d+\s+name=tag\d+>)|</DL>)')
_REGEX_HTML = ('<dt[^>]*?>(.+?)(?=<dt)')
REGEX_HTML = re.compile(_REGEX_HTML, re.I|re.S)

def extract_kakikomitxt(html):
    return re.findall(REGEX_HTML, html)


class ThreadCrawler:

    def __init__(self, INTERVAL_TIME=10, MAX_N_RETRY=10):
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

                encoding_list = ['CP932', 'euc-jp', 'utf-8']
                for encoding in encoding_list:
                    try:
                        self.html = self.res.content.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        continue

                break
            else:
                print('\nretry (ThreadCrawler.get_response())\n')
                sys.stdout.flush()
        else:
            sys.exit('Exceeded MAX_N_RETRY (WarsCrawler.get_html())')

    def extract_kakikomitxt(self):
        return extract_kakikomitxt(self.html)

    def save_html(self, savepath):
        with open(savepath, 'w') as f:
            f.write(self.html)
