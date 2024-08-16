import requests
import json


def is_twitch_online(client, secret, user):
    '''
        Checks whether a specific twitch account is currently live.

        Parameters
        ----------
        client : int
        Twitch API parameter.
        secret : int
        Twitch API parameter.
        user : int
        Username of twitch account to check.

        Returns
        ----------
            boolean: whether the twitch account is currently live

    '''
    try:
        
        #twitch api parameters
        TWITCHCLIENT_ID = client
        TWITCHSECRET = secret

        #twitch username, e.g. https://twitch.tv/Kiver would be Kiver
        USERSTREAM = user


        # URL to request OAuth Token
        tokenurl = 'https://id.twitch.tv/oauth2/token?client_id=' + TWITCHCLIENT_ID + \
                   '&client_secret=' + TWITCHSECRET+'&grant_type=client_credentials'


        response = requests.post(tokenurl)
        response.raise_for_status()
        OAuth_Token = response.json()["access_token"]

        # Connection to Twitch
        connection_response = requests.get('https://api.twitch.tv/helix/streams?user_login=' + \
                   USERSTREAM, headers={'Authorization': 'Bearer ' + \
                   OAuth_Token,'Client-Id': TWITCHCLIENT_ID})
        var=json.loads(connection_response.content)

        # print(var['data'])
        if(var['data']):
            return True
        else:
            return False

    except Exception as e: 
        print(e)
        return False