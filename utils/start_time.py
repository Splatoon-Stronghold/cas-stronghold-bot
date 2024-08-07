from pathlib import Path
import os
import time
import datetime
import json

FILENAME = "time.json"

def get_file_path() -> str:
    base_path = (Path(os.path.abspath(__file__)) /'..' /'..').resolve()
    return base_path / FILENAME

async def start_time_to_json():
    start = time.time()

    dict = {
        "start_time": start
    }

    json_object = json.dumps(dict, indent = 4)

    with open(get_file_path(), "w") as outfile:
        outfile.write(json_object)
        print("Done")

    return start
