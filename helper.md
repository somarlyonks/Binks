# HELPERS

The app server: scheduled every ->

- download the image from bing
- read user configs from mongodb
- generate pool
- push images to user's buffer folder(mailto)

## locations

/usr/local/binks
/user/local/etc/binks.conf

## interface

binks
(logged in?)
connecting...
redirect? (Y/n)

binks init 3UA-BEejvnAAAAAAAAAASSB0DXolkWxVZZyLpU0cKLqfAik-muY2bXvYIFFBMlfK
binks uninstall
binks unsubscribe
binks email
binks email somarl@live.com
binks schedule Sunday
binks schedule everyday

todo:

binks threshold 30
binks locale en_US

## oauth2

(all fake keys for illustration)

user get code:
url: https://www.dropbox.com/oauth2/authorize?client_id=5g044eviqwmlsx1&response_type=code

return: 3UA-BEejvnAAAAAAAAAASAIzOOAdn5IdtGkGwiqSKV0

exchange access token
uri: https://api.dropboxapi.com/oauth2/token?client_id=5g044eviqwmlsx1&client_secret=5g044eviqwmlsx1&grant_type=authorization_code

return: {
    'access_token': '3UA-BEejvnAAAAAAAAAASSB0DXolkWxVZZyLpU0cKLqfAik-muY2bXvYIFFBMlfK',
    'token_type': 'bearer',
    'uid': '1397873296',
    'account_id': 'dbid:AABlO4yr558u2xf6xNyRseBKpuPSlpsiVB8'
}

dbx = dropbox.Dropbox('3UA-BEejvnAAAAAAAAAASSB0DXolkWxVZZyLpU0cKLqfAik-muY2bXvYIFFBMlfK')

## mongo

### user

It's quite easy:

```json
{
    "name": "username",
    "token": "dbxtoken",
    "email": "email",
    "schedule": "Monday"
}
```

### images

I'm not sure how long will bing keep the urls alive. But it looks like a bad idea to linkage the images in mails to my server.

That means the server maybe has to backup the meta infomations of the daily images, so I need just another mongo sheet, the schema is quite easy:

```json
{
    "date": "date",
    "image": "imagename",
    "meta": "resp.image"
}
```
