import ntru_config as config

from ntru_utils.NtruEncrypt import *
from ntru_utils.Polynomial import Zx
from ntru_utils.num_to_polynomial import *

import time
import json
from datetime import timedelta
from timeit import default_timer as timer
import pandas as pd

TEST_N = 3

SNPK, SNSK = generate_keypair(config.N_P, config.N_Q, config.N_D, config.N_N)

# print(SNPK)

data = {
    "timestamp": time.time(),
    "pid": {},
}

def concatDataFrame(df, data):
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    return df


def ntruTrans(message):
    # print(message)
    characterPolynomials, N = koblitz_encoder(
        message, config.N_elliptic_a, config.N_elliptic_b)
    return characterPolynomials, N


def ntruEncrypt(message, publicKey):
    # print(f"{type(message)} -> {message}")
    characterPolynomials, N = ntruTrans(message)
    cipher_polys = []
    for element in characterPolynomials:
        cipher_text = encrypt(element, publicKey, config.N_D, N, config.N_Q)
        cipher_polys.append(cipher_text)
    return cipher_polys, N


def main():

    # create a empty dataframe with columns
    df = pd.DataFrame(columns=['Method', 'PID Length', 'Elasped Time (sec)'])

    i = 0

    while i <= TEST_N:
        t = timer()
        _, _ = ntruEncrypt(json.dumps(data), SNPK)
        # cipher_polys, n = ntruEncrypt(data, SNPK)
        elaspsed_time = timer() - t
        eval_data = {'Method': ['NTRU'], 'PID Length': [f'{i}'],
                     'Elasped Time (sec)': [timedelta(seconds=elaspsed_time)]}

        # print(eval_data)
        df = concatDataFrame(df, eval_data)


        # ====== Next Loop ======
        i += 1
        data['pid'][f'id{i}'] = "AAAA"

    print(df.head())


if __name__ == '__main__':
    main()