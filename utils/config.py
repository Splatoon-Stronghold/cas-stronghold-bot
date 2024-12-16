import json

from core.config import get_bot_config
from utils import env

config_data = get_bot_config(file_path=env.get_bot_config_path()).get_store_json()
import os
from pathlib import Path
from typing import List, Union


def get_config(key: str) -> Union[str, list]:
    """
    get_config.

    Parameters
    ----------
    key : str
        The key to access the desired data from config_data.json

    Returns
    -------
    data : str or list
        The data from config_data.json.
    """
    base_path = (Path(os.path.abspath(__file__)) / ".." / "..").resolve()
    config_path = base_path / "config_data.json"
    with open(config_path) as json_file:  # add path thing
        config_data = json.load(json_file)

    try:
        data = config_data[key]
    except Exception as e:
        print(e)
        raise KeyError(f"Key ({key}) not found in config_data.json")
    return data


def update_config(key: str, data: Union[str, list], output_file: str = None) -> Union[str, list]:
    """
    update_config.

    Parameters
    ----------
    key : str
        The key to change the desired data from config_data.json
    data : str or list
        The information to replace the current contents of the key in config_data.json
    output_file: str
        Path where the dict will be stored
    Returns
    -------
    data : str or list
        The data that was written.

    """
    base_path = (Path(os.path.abspath(__file__)) / ".." / "..").resolve()
    config_path = base_path / "config_data.json"
    with open(config_path) as json_file:  # add path thing
        config_data = json.load(json_file)

    try:
        config_data[key] = data
    except Exception as e:
        print(e)
        raise KeyError(f"Key ({key}) not found in config_data.json")

    with open(config_path, "w") as outfile:
        json.dump(config_data, outfile)

    return data


def add_channel(key: str, channel: str) -> List[Union[str, int]] | None:
    """
    add_channel.

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
    """
    data = get_config(key)

    if not isinstance(data, list):
        raise TypeError(f"The data in config_data.json with the key ({key}) was not a list of channels.")
    if channel in data:
        return  # add return
    data.append(channel)

    update_config(key, data)
    return data


def remove_channel(key: str, channel: str) -> List[Union[str, int]] | None:
    """
    remove_channel.

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
    """
    data = get_config(key)

    if not isinstance(data, list):
        raise TypeError(f"The data in config_data.json with the key ({key}) was not a list of channels.")
    if channel not in data:
        return  # add return

    data.remove(channel)

    update_config(key, data)
    return data
