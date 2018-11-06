#!/usr/bin/python3

"""
Author: Sy<somarl@live.com>
LICENSE: MIT License  Copyright (c) 2018 Sy
Tested compatible Python versions: 3.7.0b2 / 3.6.0 / 3.5.2 on Linux4.4.0
Please fire an issue at https://github.com/somarlyonks/Binks/issue if it crashes under Python3
"""

from datetime import datetime
import json
import os
import sys
from urllib import request as Q, error as E


PROTOCOL = 'https'
HOST_URL = PROTOCOL + '://www.bing.com'

PERIOD = os.getenv('BINKS_LOCAL_PERIOD', 1)
LOCAL_PATH = os.getenv('BINKS_LOCAL_PATH', '/srv/Binks/local')
TIMEOUT = int(os.getenv('BINKS_LOCAL_TIMEOUT', 5))

API = '/HPImageArchive.aspx?format=js&idx=0&mkt=en-US&ensearch=1&n=' + str(PERIOD)


def toURI(i):
    return HOST_URL + i


def GET(url):
    with Q.urlopen(toURI(url), timeout=TIMEOUT) as connect:
        if connect.status is not 200:
            raise E.HTTPError
        content = connect.read()
        if connect.headers.get_content_type() == 'application/json':
            content = content.decode(connect.headers.get_content_charset())
        return content


def persist(raw, filename):
    filepath = LOCAL_PATH + ('' if LOCAL_PATH.endswith('/') else '/') + filename
    with open(filepath, 'wb') as img:
        img.write(raw)


def download(url):
    print('[BINKS]: Downloading image -', toURI(url))
    if not url.endswith('.jpg'):
        return print('[BINKS]: Error - wrong extension name.')

    name = url.split('/')[-1]
    data = GET(url)
    persist(data, name)


def main():
    print('[BINKS]: Date:', datetime.now().strftime("%c"))
    try:
        r = GET(API)
    except E.HTTPError:
        print('[BINKS]: Error - failed to fetch api')
        sys.exit(1)
    j = json.loads(r or '{}')
    failed = []
    for img in j.get('images', []):
        try:
            download(img.get('url', ''))
        except E.HTTPError:
            print('[BINKS]: Error - wrong response for', toURI(img))
            failed.append(img)
    if len(failed):
        print('[BINKS]: retrying the failed tasks.')
        for img in failed[:]:
            try:
                download(img.get('url', ''))
                failed.pop()
            except E.HTTPError:
                print('[BINKS]: Error - wrong response for ', toURI(img), 'again.')

    print('[BINKS]: Done. Total:', PERIOD, ' Failed:', len(failed))
    sys.exit(0)


if __name__ == '__main__':
    main()
