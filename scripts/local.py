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


class Duplicated(ValueError):
    """to raise when file already exists"""
    pass


def toURI(i):
    return HOST_URL + i


def GET(url):
    with Q.urlopen(toURI(url), timeout=TIMEOUT) as connect:
        if connect.status is not 200:
            raise E.HTTPError(url, connect.status, 'Manully raised.', connect.headers, None)
        content = connect.read()
        if connect.headers.get_content_type() == 'application/json':
            content = content.decode(connect.headers.get_content_charset())
        return content


def download(url, name):
    """intentionally print the image url first and then raise exceptions"""
    print('[BINKS]: Downloading image -', toURI(url))
    if not url.endswith('.jpg'):
        return print('[BINKS]: Error - wrong extension name.')

    name += '.jpg'
    filepath = os.path.join(LOCAL_PATH, name)
    if os.path.exists(filepath):
        raise Duplicated

    data = GET(url)
    with open(filepath, 'wb') as img:
        img.write(data)


def record(img, imgname):
    filename = 'COPYRIGHTS.json'
    filepath = os.path.join(LOCAL_PATH, filename)
    cpright = img.get('copyright', '')

    if not os.path.exists(filepath):
        with open(filepath, 'wt') as f:
            f.write('[' + os.linesep + ']')

    lines = open(filepath, 'rt').readlines()
    line = '{"image": "' + imgname + '", ' + '"copyright": "' + cpright + '"}'
    if len(lines) != 2:
        line += ','
    line += os.linesep
    lines.insert(1, line)

    with open(filepath, 'wt') as f:
        f.writelines(lines)


def worker(imgs, failed, retrying=False):
    """impure: dynamically changing contexted failed list"""
    if retrying and len(failed):
        print('[BINKS]: Retrying the failed tasks.')
    for img in imgs:
        try:
            url = img.get('url', '')
            name = url.split('/')[-1].split('_')[0]
            download(url, name)
            if retrying:
                failed.pop()
        except E.HTTPError:
            print('[BINKS]: Error - wrong response for', toURI(url))
            if not retrying:
                failed.append(img)
        except Duplicated:
            print('[BINKS]: Image exists -', os.path.join(LOCAL_PATH, name + '.jpg'))
        else:
            record(img, name)


def main():
    print('[BINKS]: Date:', datetime.now().strftime("%c"))
    try:
        r = GET(API)
    except E.HTTPError:
        print('[BINKS]: Error - failed to fetch api')
        sys.exit(1)

    j = json.loads(r or '{}')
    images = j.get('images', [])
    failed = []

    worker(images, failed)
    worker(failed[:], failed, retrying=True)

    print('[BINKS]: Done. Total:', len(images), ' Failed:', len(failed))
    sys.exit(0)


if __name__ == '__main__':
    main()
