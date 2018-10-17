"""
TODO
  proxy
"""


import json
import os

import dropbox

from utils import q_get, stopwatch, HOST_URL


API = '/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US&ensearch=1'
PROXY = 'http://localhost:8123'


def upload(dbx, data, name, overwrite=False):
    path = 'bing/buffer'
    mode = (dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add)

    with stopwatch('uploading %d bytes' % len(data)):
        try:
            res = dbx.files_upload(data, path, mode, mute=True)
        except dropbox.exceptions.ApiError as err:
            return print('[DORPBOX]: API error - ', err)
    print('[DROPBOX]: uploaded as', res.name.encode('utf8'))
    return res


def download(dbx, url):
    print(f'[BING]: Downloading image - {HOST_URL + url}')
    if not url.endswith('.jpg'):
        return print(f'[BING]: Error - wrong extension name.')

    name = url.split('/')[-1]
    data = q_get(url)
    upload(dbx, data.content, name)


def worker(token):
    try:
        dbx = dropbox.Dropbox(token)
    except AssertionError:
        print(f'[DROPBOX]: Invalid token - <{token}>')
        return

    os.environ['https_proxy'] = PROXY
    r = q_get(API)
    j = json.loads(r and r.text or '{}')
    for img in j.get('images', []):
        download(dbx, img.get('url', ''))
