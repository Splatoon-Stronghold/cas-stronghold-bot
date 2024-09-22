import os
import sys
import dotenv

dotenv.load_dotenv()

def get_env_var(name: str) -> str:
    '''get_env_var
    Parameters
    ----------
    name : str
        The name of the environment variable to access.
    Returns
    -------
    value : str
        The value of the environment variable.
    '''
    try:
        value = os.getenv(name)
        if value is not None:
            return value
        else:
            print(f'Value of {name} is empty. Exiting')
            sys.exit(1)
    except Exception as e:
        print(f'Could not get value of {name} due to {e}. Exiting')
        sys.exit(1)

# Discord

def get_discord_token() -> str:
    return get_env_var('DISCORD_TOKEN')

def get_guild_id() -> int:
    return int(get_env_var('GUILD_ID'))

# Twitch

def get_twitch_client() -> str:
    return get_env_var("TWITCH_CLIENT")

def get_twitch_secret() -> str:
    return get_env_var("TWITCH_SECRET")

def get_twitch_user() -> str:
    return get_env_var("TWITCH_USER")

# YouTube

def get_yt_api_key() -> str:
    return get_env_var("YT_API_KEY")

def get_yt_channel_id() -> str:
    return get_env_var("YT_CHANNEL_ID")

# Logging channel
def get_logging_channel_id() -> str:
    return get_env_var("LOGGING_CHANNEL_ID")