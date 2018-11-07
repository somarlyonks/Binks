# Binks

A script for downloading bing desktops. @see [LOCAL](##LOCAL)

Or you can install the dropbox app. @see [APP](##APP)

## LOCAL

Script: [scripts/local.py](scripts/local.py)

This script is used by Binks dropbox app server to fetch raw pictures. As it's designed to be portable and compatible with most versions of Python3, you can also run it locally by registering a schedule with _crontab_. like:

`0 11 * * * /home/sy/Devel/Binks/scripts/local.py`

after adding excute permission to the script.

But it only save the images on your hardware.

### Configs with environment variables

__BINKS_LOCAL_PERIOD__ : Period of the script (runs every _???_ days), default: `1`

__BINKS_LOCAL_PATH__ : Path to save images, default: `/srv/Binks/local`

__BINKS_LOCAL_TIMEOUT__ : Timeout of trying connect, default: `5`

### Copyrights of the images

Uses of these Bing images are restricted to wallpaper only. The specific copyright infomations will be saved in the `BINKS_LOCAL_PATH` directory named `COPYRIGHTS.json` with the schema like:

```json
[{
    "image": "AutumnNeuschwanstein",
    "copyright": "Neuschwanstein Castle in southern Bavaria, Germany (© Boris Jordan Photography/Getty Images)"
}]
```

@see [scripts/example.json]('scripts/example.json').

## APP

TODO

## DEV

The local script is supposed to be portable and compatible with all versions of Python3 __without dependencies__.

### App with python3.7.0b2

With pyenv and virtualenvwrapper

```shell
pyenv install 3.7.0b2
mkvirtualenv binks --python=/home/sy/.pyenv/versions/3.7.0b2/bin/python3.7
pip install -r requirements.txt
```

## LICENSE

### Files of this repo

MIT License  Copyright (c) 2018 Sy.

### Images from bing.com

Uses of the Bing images are restricted to wallpaper only. Check [bing.com](https://bing.com) for more informations about constrains of the usage of the images.
