#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import requests


REGEX_HTML = ('<dt>(\d+) ：([^：]+)：'
              '(\d+)/(\d+)/(\d+)\((.)\) (\d+):(\d+):([\d\.]+) '
              'ID:([\w\+/]+)(?:(?:.(?!=<dd>))+.)?<dd> (.+)')


class ThreadCrawler:

    def __init__(self, INTERVAL_TIME=3, MAX_N_RETRY=10):
        self.res = None
        self.INTERVAL_TIME = INTERVAL_TIME
        self.MAX_N_RETRY = MAX_N_RETRY

    def get_response(self, url):
        '''指定したurlのhtmlを取得する
        '''
        time.sleep(self.INTERVAL_TIME)

        for n in range(self.MAX_N_RETRY):
            time.sleep(10 * n * self.INTERVAL_TIME)

            try:
                res = requests.session().get(url)
            except requests.ConnectionError:
                print('\nConnection aborted.\n')
                res = None

            if res and res.status_code == 200:
                self.res = res
                break
            else:
                print('\nretry (2chCrawler.get_html())\n')
                sys.stdout.flush()
        else:
            sys.exit('Exceeded MAX_N_RETRY (WarsCrawler.get_html())')


    def extract_kifutxt(self):
        html = self.res.content.decode('CP932')
        return re.findall(REGEX_HTML, html)
