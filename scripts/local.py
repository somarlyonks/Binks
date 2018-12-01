#!/usr/bin/python3

"""
Author: Sy<somarl@live.com>
LICENSE: MIT License  Copyright (c) 2018 Sy
Tested compatible Python versions: 3.7.0b2 / 3.6.0 / 3.5.2 on Linux4.4.0
Please fire an issue at https://github.com/somarlyonks/Binks/issue if it crashes under Python3
"""

from __future__ import print_function

from datetime import datetime
from functools import partial
import getpass
import json
import os
import socket
import sys


CEND = '\33[0m'
F_COLORED = lambda color: lambda str: color + str + CEND  # noqa
CRED = F_COLORED('\33[91m')
CGREEN = F_COLORED('\33[92m')
CYELLOW = F_COLORED('\33[93m')

PID = os.getpid()
PID_SEG = 'BINKS[' + str(PID) + ']:'
HOSTNAME = socket.gethostname()
USERNAME = getpass.getuser()
USERNAME_SEG = '(' + USERNAME + ')'
F_GETTIME = lambda : ' '.join(datetime.now().ctime().split(' ')[1: -1])  # noqa
F_STD_SEGS = lambda : F_GETTIME() + ' ' + HOSTNAME + ' ' + PID_SEG + ' ' + USERNAME_SEG  # noqa

PY_VERSION = sys.version_info
try:
    assert PY_VERSION.major == 3
    from urllib import request as Q, error as E, parse as P
except AssertionError:
    sys.stderr.write(F_STD_SEGS() + ' ' + CRED('Error') + ' - Python3 required\n')
    sys.exit(1)
try:
    assert PY_VERSION.minor >= 3
    _print = partial(print, flush=True)
except AssertionError:
    sys.stdout.write(F_STD_SEGS() + ' ' + CYELLOW('Warning') + '- Python3.3.0+ prefered\n')
    _print_ = print

    def _print(*args, **kwargs):
        flush = kwargs.pop('flush', True)
        _print_(*args, **kwargs)
        if flush:
            kwargs.get('file', sys.stdout).flush()


def print(*args, **kwargs):
    level = kwargs.pop('level', None)
    __print = partial(_print, F_STD_SEGS())
    if level == 'error':
        __print(CRED('Error'), '-', *args, **kwargs)
    elif level == 'warning':
        __print(CYELLOW('Warning'), '-', *args, **kwargs)
    elif level == 'info':
        __print(CGREEN(args[0]), '-', *args[1:], **kwargs)
    else:
        __print(*args, **kwargs)


SCHEME = 'https'
HOST_URL = SCHEME + '://' + 'www.bing.com'

PERIOD = os.getenv('BINKS_LOCAL_PERIOD', 1)
LOCAL_PATH = os.getenv('BINKS_LOCAL_PATH', '/srv/Binks/local')
TIMEOUT = int(os.getenv('BINKS_LOCAL_TIMEOUT', 5))

API = '/HPImageArchive.aspx?format=js&idx=0&mkt=en-US&ensearch=1&n=' + str(PERIOD)


class Duplicated(ValueError):
    """to raise when file already exists"""
    pass


def toURI(i):
    return P.urljoin(HOST_URL, i)


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
    print('Downloading image:', toURI(url))
    if not url.endswith('.jpg'):  # just for guard, there's no need to raise for it
        return print('wrong extension name', level='error')

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
    line = json.dumps({'image': imgname, 'copyright': cpright}, sort_keys=True)
    if len(lines) != 2:
        line += ','
    line += os.linesep
    lines.insert(1, line)

    with open(filepath, 'wt') as f:
        f.writelines(lines)


def worker(imgs, failed, retrying=False):
    """impure: dynamically changing contexted failed list"""
    if retrying and len(failed):
        print('Retrying the failed tasks')
    for img in imgs:
        try:
            url = img.get('url', '')
            name = url.split('/')[-1].split('_')[0]
            download(url, name)
            if retrying:
                failed.pop()
        except E.HTTPError:
            print('wrong response for', toURI(url), level='error')
            if not retrying:
                failed.append(img)
        except Duplicated:
            print('image exists:', os.path.join(LOCAL_PATH, name + '.jpg'), level='warning')
            if retrying:
                failed.pop()
        else:
            record(img, name)


def main():
    print('Begin', USERNAME_SEG, level='info')
    try:
        r = GET(API)
    except E.HTTPError:
        print('failed to fetch api', level='error')
        sys.exit(1)

    j = json.loads(r or '{}')
    images = j.get('images', [])
    failed = []

    worker(images, failed)
    worker(failed[:], failed, retrying=True)

    print('Done', 'Total:', len(images), ' Failed:', len(failed), level='info')
    sys.exit(0)


if __name__ == '__main__':
    main()
