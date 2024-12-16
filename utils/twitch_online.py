import json
from typing import Union

import requests


def is_twitch_online(client: Union[int, str], secret: Union[int, str], user: Union[int, str]) -> bool:
    """
    Checks whether a specific twitch account is currently live.

    Parameters
    ----------
    client : int|str
    Twitch API parameter.
    secret : int|str
    Twitch API parameter.
    user : int|str
    Username of twitch account to check.

    Returns
    ----------
        boolean: whether the twitch account is currently live

    """
    try:

        # URL to request OAuth Token
        tokenurl = (
            "https://id.twitch.tv/oauth2/token?client_id="
            + client
            + "&client_secret="
            + secret
            + "&grant_type=client_credentials"
        )

        response = requests.post(tokenurl)
        response.raise_for_status()
        oauth_token = response.json()["access_token"]

        # Connection to Twitch
        connection_response = requests.get(
            "https://api.twitch.tv/helix/streams?user_login=" + user,
            headers={"Authorization": "Bearer " + oauth_token, "Client-Id": client},
        )
        var = json.loads(connection_response.content)

        if var["data"]:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False
