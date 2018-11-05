#

from datetime import datetime
import json
import os
import sys
from urllib import request as Q, error as E


PROTOCOL = 'https'
HOST_URL = f'{PROTOCOL}://www.bing.com'

FREQUENCY = os.getenv('BINKS_LOCAL_FREQUENCY', 1)
LOCAL_PATH = os.getenv('BINKS_LOCAL_PATH', '/srv/Binks/local')
TIMEOUT = os.getenv('BINKS_LOCAL_TIMEOUT', 5)

API = '/HPImageArchive.aspx?format=js&idx=0&mkt=en-US&ensearch=1&n=' + str(FREQUENCY)


def GET(url):
    with Q.urlopen(HOST_URL + url, timeout=TIMEOUT) as connect:
        if connect.status is not 200:
            raise E.HTTPError
        return connect.read()


def persist(raw, filename):
    filepath = LOCAL_PATH + ('' if LOCAL_PATH.endswith('/') else '/') + filename
    with open(filepath, 'wb') as img:
        img.write(raw)


def download(url):
    print(f'[BINKS]: Downloading image - {HOST_URL + url}')
    if not url.endswith('.jpg'):
        return print('[BINKS]: Error - wrong extension name.')

    name = url.split('/')[-1]
    data = GET(url)
    persist(data, name)


def main():
    print(f'[BINKS]: Date: {datetime.now().strftime("%c")}')
    try:
        r = GET(API)
    except E.HTTPError:
        print(f'[BINKS]: Error - failed to fetch api')
        sys.exit(1)
    j = json.loads(r or '{}')
    failed = []
    for img in j.get('images', []):
        try:
            download(img.get('url', ''))
        except E.HTTPError:
            print(f'[BINKS]: Error - wrong response for {HOST_URL + img}')
            failed.append(img)
    if len(failed):
        print('[BINKS]: retrying the failed tasks.')
        for img in failed[:]:
            try:
                download(img.get('url', ''))
                failed.pop()
            except E.HTTPError:
                print(f'[BINKS]: Error - wrong response for {HOST_URL + img} again.')

    print(f'[BINKS]: Total: {FREQUENCY} , Failed: {len(failed)}')
    sys.exit(0)


if __name__ == '__main__':
    main()
