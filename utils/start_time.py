from pathlib import Path
import os
import time
import datetime
import json

async def save_start_time():
    dict = {
        "start_time": time.time()
    }

    json_object = json.dumps(dict, indent = 4)

    base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
    path = base_path / 'time.json'
    with open(path, "w") as json_file:
        json_file.write(json_object)

def get_start_time() -> datetime.datetime:
    '''get_start_time
    Returns
    -------
    data : datetime.datetime
        The timestamp when the bot was started (which is saved in time.json).
    '''

    base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
    path = base_path / 'time.json'
    with open(path) as json_file:
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
