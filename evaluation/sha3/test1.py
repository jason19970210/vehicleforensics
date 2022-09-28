from datetime import timedelta
from hashlib import sha3_256
import time
from timeit import default_timer as timer
import sys
import json

data = {
    "timestamp": time.time(),
    "pid": {}, # "id1": "AAAA"
}

# Measure function elasped time in Python
# https://stackoverflow.com/a/55239060
def main():
    i = 0
    while i <= 100:
        t = timer() # start timer
        sha3_256().update(json.dumps(data).encode()) # encode() with default 'utf-8'
        elaspsed_time = timer() - t # calculate time duration

        print(f"i: {i:4},  pid len : {len(data['pid']):4},  elaspsed time: {timedelta(seconds=elaspsed_time)} sec(s),  size: {data['pid'].__sizeof__()} bytes")

        # Next loop
        i += 1
        # add a item into `pid`
        data['pid'][f'id{i}'] = "AAAA"

if __name__ == '__main__':
    main()