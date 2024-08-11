from pathlib import Path
from typing import Union
import os
import json

from core.config import load_bot_config_from_file, generate_bot_config

try:
    base_path = (Path(os.path.abspath(__file__)) / '..' / '..').resolve()
    config_path = base_path / 'config_data.json'
    config_data = load_bot_config_from_file(config_path.__str__()).get_store_json()
except FileNotFoundError as fe:
    print(fe)
    print("BotConfig error: config_data.json file not found, generating new instance")
    config_data = generate_bot_config({
            "youtube_announcement_channels": ["announcements"],
            "vod_count": 0,  # If the file does not exists evaluate getting this value from a DB
            "yt_text_channel_id": 1132053178838421554,
            "twitch_announcement_channels": {},
            "publish_announcement_channels": ["announcements"]
        }
    ).get_store_json()


def get_config(key : str) -> Union[str, list]:
    '''get_config
    Parameters
    ----------
    key : str
        The key to access the desired data from config_data.json
    Returns
    -------
    data : str or list
        The data from config_data.json.
    '''

    # TODO: We obtain the data from BotConfig
    # base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
    # config_path = base_path / 'config_data.json'
    # with open(config_path) as json_file: # add path thing
    #     config_data = json.load(json_file)
    
    try:
        data = config_data[key]
    except:
        raise KeyError(f'Key ({key}) not found in config_data.json')
    return data


def update_config(key : str, data : Union[str, list]) -> Union[str, list]:
    '''update_config
    Parameters
    ----------
    key : str
        The key to change the desired data from config_data.json
    data : str or list
        The information to replace the current contents of the key in config_data.json
    Returns
    -------
    data : str or list
        The data that was written.
    '''
    base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
    config_path = base_path / 'config_data.json'
    with open(config_path) as json_file: # add path thing
        config_data = json.load(json_file)
    
    try:
        config_data[key] = data
    except:
        raise KeyError(f'Key ({key}) not found in config_data.json')
    
    with open(config_path, "w") as outfile:
        json.dump(config_data, outfile)

    return data

def add_channel(key : str, channel : str):
    '''add_channel
    Parameters
    ----------
    key : str
        The key to change the desired data from config_data.json. Note - the key must reference a list of channels. 
        TypeError will be raised if it does not reference a list of channels.
    channel : str
        The channel to be added
    Returns
    -------
    data : list
        List of channels with the new channel.
    '''
    data = get_config(key)

    if type(data) != list:
        raise TypeError(f'The data in config_data.json with the key ({key}) was not a list of channels.')
    if channel in data:
        return # add return
    data.append(channel)

    update_config(key, data)
    return data


def remove_channel(key : str, channel : str):
    '''remove_channel
    Parameters
    ----------
    key : str
        The key to change the desired data from config_data.json. Note - the key must reference a list of channels. 
        TypeError will be raised if it does not reference a list of channels.
    channel : str
        The channel to be added
    Returns
    -------
    data : list
        List of channels without the one removed.
    '''
    data = get_config(key)

    if type(data) != list:
        raise TypeError(f'The data in config_data.json with the key ({key}) was not a list of channels.')
    if channel not in data:
        return # add return
    
    data.remove(channel)

    update_config(key, data)
    return data


