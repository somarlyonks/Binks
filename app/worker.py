"""
TODO
  proxy
"""


import json

import dropbox

from utils import q_get, stopwatch, Proxy, HOST_URL


class BinksWorker(dropbox.Dropbox):
    BINKS_PATH = 'bing/buffer'
    BING_API = '/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US&ensearch=1'

    def __init__(self, oauth_token, proxy='http://localhost:8123'):
        super(BinksWorker, self).__init__(oauth_token)
        self.https_proxy = proxy

    @Proxy
    def binks_work(self):
        r = q_get(self.BING_API)
        j = json.loads(r and r.text or '{}')
        for img in j.get('images', []):
            self.binks_download(img.get('url', ''))

    def binks_download(self, url):
        print(f'[BING]: Downloading image - {HOST_URL + url}')
        if not url.endswith('.jpg'):
            return print(f'[BING]: Error - wrong extension name.')

        name = url.split('/')[-1]
        data = q_get(url)
        self.binks_upload(data.content, name)

    def binks_upload(self, data, name, overwrite=False):
        mode = (dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add)

        with stopwatch('uploading %d bytes' % len(data)):
            try:
                res = self.files_upload(data, self.BINKS_PATH, mode, mute=True)
            except dropbox.exceptions.ApiError as err:
                return print('[DORPBOX]: API error - ', err)
        print('[DROPBOX]: Uploaded as', res.name.encode('utf8'))
        return res
