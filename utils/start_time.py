from pathlib import Path
import os
import time
import datetime
import json

def get_file_path() -> str:
    '''get_file_path
    Returns
    -------
    data : str
        The file path to time.json.
    '''

    base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
    return base_path / 'time.json'

async def save_start_time():
    dict = {
        "start_time": time.time()
    }

    json_object = json.dumps(dict, indent = 4)

    with open(get_file_path(), "w") as json_file:
        json_file.write(json_object)
        print("Done")

def get_start_time() -> datetime.datetime:
    '''get_start_time
    Returns
    -------
    data : datetime.datetime
        The timestamp when the bot was started, saved in time.json.
    '''

    with open(get_file_path()) as json_file:
        data = json.load(json_file)

    return datetime.datetime.fromtimestamp(data["start_time"])

def get_uptime() -> float:
    '''get_uptime
    Returns
    -------
    data : float
        The time in seconds since the bot was started.
    '''

    end_time = datetime.datetime.fromtimestamp(time.time())
    duration = end_time - get_start_time()

    return duration.total_seconds()
