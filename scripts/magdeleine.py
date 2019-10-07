#!/home/sy/.virtualenvs/binks/bin/python

"""
Author: Sy<somarl@live.com>
LICENSE: MIT License  Copyright (c) 2018 Sy

For personal use actually. Place it here to illustrate how to customize
the local.py for specific sites.
"""

import getpass
import json
import os
import socket
import sys
from datetime import datetime
from functools import partial
from html.parser import HTMLParser

import requests as Q


CEND = '\33[0m'
F_COLORED = lambda color: lambda str: color + str + CEND  # noqa
F_CRED = F_COLORED('\33[91m')
F_CGREEN = F_COLORED('\33[92m')
F_CYELLOW = F_COLORED('\33[93m')

PID = os.getpid()
PID_SEG = 'MGDL[' + str(PID) + ']:'
HOSTNAME = socket.gethostname()
USERNAME = getpass.getuser()
USERNAME_SEG = '(' + USERNAME + ')'
F_GETTIME = lambda : ' '.join(datetime.now().ctime().split(' ')[1: -1])  # noqa
F_STD_SEGS = lambda : F_GETTIME() + ' ' + HOSTNAME + ' ' + PID_SEG + ' ' + USERNAME_SEG  # noqa


_print = partial(print, flush=True)


def print(*args, **kwargs):
    kwargs.pop('flush', None)
    level = kwargs.pop('level', None)
    __print = partial(_print, F_STD_SEGS())

    if level == 'error':
        __print(F_CRED('Error'), '-', *args, **kwargs)
    elif level == 'warning':
        __print(F_CYELLOW('Warning'), '-', *args, **kwargs)
    elif level == 'info':
        info, *args = args
        __print(F_CGREEN(info), '-', *args, **kwargs)
    else:
        __print(*args, **kwargs)


class MgParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if (tag == 'body'):
            body_style = next((value for (attr, value) in attrs if attr == 'style'))
            self.mg_url = body_style.split("'")[1]
        if (tag == 'img'):
            self.mg_author_avatar = next((value for (attr, value) in attrs if attr == 'src'))

    def handle_data(self, data):
        if self.lasttag == 'h2':
            self.mg_author = data


SCHEME = 'https'
HOST_URL = SCHEME + '://' + 'magdeleine.co'

LOCAL_PATH = os.getenv('MAGDELEINE_DOWNLOADER_PATH', '/home/sy/Desktop')
TIMEOUT = int(os.getenv('MAGDELEINE_DOWNLOADER_TIMEOUT', 25))


class Duplicated(ValueError):
    """to raise when file already exists"""
    pass


def GET(url):
    r = Q.get(url, timeout=TIMEOUT, stream=True)
    r.raise_for_status()

    return r


def download(url, name):
    """intentionally print the image url first and then raise exceptions"""
    print('Downloading image:', url)
    if not url.endswith('.jpg'):
        print('wrong extension name', level='error')

    filepath = os.path.join(LOCAL_PATH, name)
    if os.path.exists(filepath):
        raise Duplicated

    data = GET(url).content
    with open(filepath, 'wb') as img:
        img.write(data)


def record(img, author, avatar):
    filename = 'meta.json'
    filepath = os.path.join(LOCAL_PATH, filename)

    if not os.path.exists(filepath):
        with open(filepath, 'wt') as f:
            f.write('[' + os.linesep + ']')

    lines = open(filepath, 'rt').readlines()
    line = json.dumps({'image': img, 'author': {'name': author, 'avatar': avatar}}, sort_keys=True)
    if len(lines) != 2:
        line += ','
    line += os.linesep
    lines.insert(1, line)

    with open(filepath, 'wt') as f:
        f.writelines(lines)


def worker(parsed):
    url = parsed.mg_url
    name = url.split('/')[-1]
    try:
        download(url, name)
    except Q.HTTPError:
        print('wrong response for', url, level='error')
    except Duplicated:
        print('image exists:', os.path.join(LOCAL_PATH, name), level='warning')
    else:
        record(url, author=parsed.mg_author, avatar=parsed.mg_author_avatar)
        pass


def main():
    print('Begin', USERNAME_SEG, level='info')
    try:
        r = GET(HOST_URL)
    except Q.HTTPError:
        print('failed to fetch api', level='error')
        sys.exit(1)

    p = MgParser()
    p.feed(r.text)

    worker(p)

    print('Done', 'exit.', level='info')
    sys.exit(0)


if __name__ == '__main__':
    main()
