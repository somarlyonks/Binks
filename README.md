# Binks

A script for downloading bing desktops. @see [LOCAL](##LOCAL)

Or you can install the dropbox app. @see [APP](##APP)

## LOCAL

Script: [scripts/local.py](scripts/local.py)

This script is used by Binks dropbox app server to fetch raw pictures. As it's designed to be portable and compatible with most versions of Python3, you can also run it locally by registering a schedule with _crontab_. like appending:

```cron
BINKS_LOCAL_PATH=/home/sy/Dropbox/bing/buffer
0 10 * * * root /home/sy/Desktop/sy/env/Binks/scripts/local.py >> /var/log/cron.log 2>&1
1 10 * * 7 root export BINKS_LOCAL_PERIOD=7 && /home/sy/Desktop/sy/env/Binks/scripts/local.py >> /var/log/cron.log 2>&1
```

to the `/etc/crontab`. You can cat log in `/var/log/cron.log` like:

```stdout
...
Dec  1 10:00:01 envy CRON[30529]: (smmsp) CMD (test -x /etc/init.d/sendmail && test -x /usr/share/sendmail/sendmail && test -x /usr/lib/sm.bin/sendmail && /usr/share/sendmail/sendmail cron-msp)
Dec  1 10:00:01 envy CRON[30528]: (root) CMD (/home/sy/Desktop/sy/env/Binks/scripts/local.py >> /var/log/cron.log 2>&1)
Dec  1 10:00:01 envy BINKS[30536]: (root) Begin - (root)
Dec  1 10:00:01 envy BINKS[30536]: (root) Downloading image: https://www.bing.com/az/hprichbg/rb/KilchurnSky_EN-CN9115024751_1920x1080.jpg
Dec  1 10:00:01 envy BINKS[30536]: (root) Done - Total: 1  Failed: 0
Dec  1 10:05:01 envy CRON[31889]: (root) CMD (command -v debian-sa1 > /dev/null && debian-sa1 1 1)
...
```

Notice that the path is set to `BINKS_LOCAL_PATH=/home/sy/Dropbox/bing/buffer`, so Dropbox will auto sync the folder after downloading.

Of course, if your computer or server is not running everyday or even not every week and you don't want to write adpator scripts for anacron to lanuch the local downloading script, you can just subscribe to the Binks app and setup your preferences.

Or you may access to my [Dropbox/bing](https://www.dropbox.com/sh/t89049ikchjzmz2/AADN5fxvLgjmggqrQfI57j37a?dl=0) and view or download images mannully from there.

### Configs with environment variables

__BINKS_LOCAL_PERIOD__ : Period of the script (runs every _???_ days), default: `1`, should be within: `[1, 8] & Z`

__BINKS_LOCAL_PATH__ : Path to save images, default: `/srv/Binks/local`

__BINKS_LOCAL_TIMEOUT__ : Timeout of trying connect, default: `5`

### Copyright infomations of the images

Uses of these Bing images are restricted to wallpaper only. The specific copyright infomations will be saved in the `BINKS_LOCAL_PATH` directory named `COPYRIGHTS.json` with the schema like:

```json
[{
    "image": "AutumnNeuschwanstein",
    "copyright": "Neuschwanstein Castle in southern Bavaria, Germany (© Boris Jordan Photography/Getty Images)"
}]
```

@see [scripts/example.json](scripts/example.json).

### Customizing & for sites other than Bing

The local script is flexible, you can always directly change it as you like.

As uses of Bing images are restricted, you may want to deploy the script for other sites with CC-family liscenses. Check the [scripts/magdeleine.py](scripts/magdeleine.py) as an example for customizing which downloads images from [magdeleine.co](https://magdeleine.co).

You may find that I used `requests` and specify the virtualenv in that script and delete all the verbose contents for compatiblities. You can also use `xpath`/`BeautifulSoup`/`PyQuery` .etc parser libs instead of the toy `MgParser` in the script.

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
