from datetime import timedelta
from hashlib import sha3_256, sha3_384, sha3_512
import time
from timeit import default_timer as timer
import json
import pandas as pd

TEST_N = 5

data = {
    "timestamp": time.time(),
    "pid": {},
}

def concatDataFrame(df, data):
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    return df


def main():

    # create a dataframe(excel) with column names
    df = pd.DataFrame(columns=['Method', 'Length', 'Elasped Time (sec)'])

    i = 0
    while i <= TEST_N:

        # Method 1 : SHA3-256
        t = timer()
        sha3_256().update(json.dumps(data).encode())
        elaspsed_time = timer() - t

        eval_data = {'Method': ['SHA3-256'], 'Length': [f'{i}'],
                     'Elasped Time (sec)': [f'{timedelta(seconds=elaspsed_time)}']}
        # print(eval_data)
        # df = pd.concat([df, pd.DataFrame(eval_data)], ignore_index=True)
        df = concatDataFrame(df, eval_data)


        # Method 2 : SHA3-384
        t = timer()
        sha3_384().update(json.dumps(data).encode())
        elaspsed_time = timer() - t

        eval_data = {'Method': ['SHA3-384'], 'Length': [f'{i}'],
                     'Elasped Time (sec)': [f'{timedelta(seconds=elaspsed_time)}']}
        # print(eval_data)
        df = concatDataFrame(df, eval_data)

        # Method 3 : SHA3-512
        t = timer()
        sha3_512().update(json.dumps(data).encode())
        elaspsed_time = timer() - t

        eval_data = {'Method': ['SHA3-512'], 'Length': [f'{i}'],
                     'Elasped Time (sec)': [f'{timedelta(seconds=elaspsed_time)}']}
        # print(eval_data)
        df = concatDataFrame(df, eval_data)

        # ====== Next Loop ======
        i += 1
        data['pid'][f'id{i}'] = "AAAA"
    
    print(df.head())

    ## Plot


if __name__ == '__main__':
    main()
