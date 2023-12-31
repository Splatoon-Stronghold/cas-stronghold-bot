import time
import json

FILENAME = "time.json"

async def start_time_to_json():
    start = time.time()

    dict = {
        "start_time": start
    }

    json_object = json.dumps(dict, indent = 4)

    with open(FILENAME, "w") as outfile:
        outfile.write(json_object)
        print("Done")

    return start