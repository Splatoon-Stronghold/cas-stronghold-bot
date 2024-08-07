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

