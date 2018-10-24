# HELPERS

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
