import time
import json
from hashlib import sha3_256
from datetime import datetime, timedelta
from timeit import default_timer as timer
import pandas as pd

# add utils folder to sys path
import sys
from pathlib import Path
sys.path.append(Path(__file__).parents[2].as_posix())

from utils.ntru_utils.NtruEncrypt import *
from utils.ntru_utils.Polynomial import Zx
from utils.ntru_utils.num_to_polynomial import *

import ntru_nconfig as nconfig


TEST_N = 1

SNPK, SNSK = generate_keypair(nconfig.N_P, nconfig.N_Q, nconfig.N_D, nconfig.N_N)

# print(SNPK)

# data = {
#     "timestamp": time.time(),
#     "pid": {},
# }

# data = f"{time.time()}"
# data = f"{datetime.now()}:31:AB"
# data = f"{time.time()}:31:ABAA:DDAA:0CAA:E4AA:23AA"

# print(f"{data}")


def concatDataFrame(df, data):
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    return df


def ntruTrans(message):
    # print(message)
    characterPolynomials, N = koblitz_encoder(
        message, nconfig.N_elliptic_a, nconfig.N_elliptic_b)
    return characterPolynomials, N


def ntruEncrypt(message, publicKey):
    # print(f"{type(message)} -> {message}")
    characterPolynomials, N = ntruTrans(message)
    cipher_polys = []
    for element in characterPolynomials:
        cipher_text = encrypt(element, publicKey, nconfig.N_D, N, nconfig.N_Q)
        cipher_polys.append(cipher_text)
    return cipher_polys, N


def ntruDecrypt(cipherPolys, privateKey, n):
    dec_w = []
    for element in cipherPolys:
        decrypted_message = decrypt(
            element, privateKey, nconfig.N_P, nconfig.N_Q, n)
        # print(decrypted_message.print_polynomial())
        dec_w.append(decrypted_message.coeffs)
    decrypted_plain_text = koblitz_decoder(points_decoder(dec_w))
    # print(decrypted_plain_text)
    return decrypted_plain_text


def main():

    # PID init
    # desirePIDList = ['0C', '0D']

    # Data init
    data = ",04:A,0C:AA,0D:A,11:A"
    # data = "1654273410.7560978,b'NIhMjsINY1rsvG7W7PcKbk3Gsie7h8wXHcIGWDysbpwBrDGw4nSzyPyESVD2DLo1lDsNWpjdw+SKh+TiQAAA',PID1:AAAA"
    # data = "NIhMjsINY1rsvG7W7PcKbk3Gsie7h8wXHcIGWDysbpwBrDGw4nSzyPyESVD2DLo1lDsNWpjdw+SKh+TiQAA"
    # data = '010011100100111001110010011100110100011001001010001101000100100001010111011001110010111101110100010011000111001101010001011101100101001101101110011000110100011001100111011010100111100101101110011100000011100101110111010110010110110001110010001100000100101101001100011101010111000100110111010000110110110100110111010011110011010101000100001100000011001101101000011000100100001001010010010100010110101001010100001100000110111101010101011001010011100001101101011001100100101101100001001110000010101101101100011100000111011000111001011110010110111101101001001100010011100001101101011000100101000001010010011100010111000101001101010110010111100101000001010000010100000101000001010011100100010001111010010011110011001000101011011001110101000001010100010110100101001000110000010010010110011001010101010000100100111100111001010010000111100000111000010101010011000000110011010011100101100001010000010101000010111101101001010101000011100001001001010101100100111101010001010100110100011001010100011110100100010000110010010001110111010000110111001110010100101101100110011100110111010001000100010101000111011001110010001110000110001101010010010101010011010001000011010001100111010001101111010100110011001101110001010010010111000001110011011110100100001100110000011000100110001000101111010001000111101000110000011100010011100101110111010000010100000101000001010011100100111101011000011110000110010100110110010001010110110001001011010011110101100100110011011101010100010001010010010110010100010101001110011000010100100000110101010001100111000101010000010000100011010101111000011000110100111001000011011110010100101101011010011011100101101001011001001110000110010101111000010100110100110001000010011000110111001000110011010011010101100100110111010101100100001101100100010010010111011000110001011001010010111101100111010011110101001101010001011100000110110001000101010010110111010000101011011101010101100100101011010001010101101000110110011011010111000001000101011101100101010001000110010010010100101001000001010000010100000101000001010011100100111101001111011100110110001101110111001101110011010001001100011101100101010001001101011001010110101001110010001100100101001001010010001110000110001101010101001100000101011100110110011110100111001100101111010011110110101101001011010001100110011001101011011011110100100001010000001011110100111001010001011001000100001101010101001110000111011001101010011010010111000100110110001110010110010101100101011010000101010001010000001101000100111100110011001100110101000100101011011001100011100101110010011011100110111101110110011011100101100100110110010100110110101001010001001100010111000001110011011000110111100001100010001010110101000101000001010000010100000101000001'
    # data = b'4\x16\xcc[Z2\xe8\xaf8\xcd\xab\xd5\x9e\xb5X \x89\x8dh)Cv\x94\xff\xdb\x01!\xb6\xb1W\xd0_&{z\x92\xf6<\xb8\xbeV%\xca\x9a\xbeGoI\xad\xa0\xacU|EYdd\xe1"?\x00\x00\x00'

    ## will cause decrypt failed data
    # data = f"{{}}" ## Due to 'f string', the output will be '{}' as well

    # create a empty dataframe with columns
    df = pd.DataFrame(columns=['Method', 'PID Length', 'Elasped Time (sec)'])

    i = 0

    while i < TEST_N:
        t = timer()
        
        print(f"data: {data}")

        # Data Hash -> SHA3-256
        h = sha3_256()
        h.update(data.encode())
        # h.update(data)
        print(f"hash: {h.hexdigest()}")

        # _, _ = ntruEncrypt(json.dumps(data), SNPK)
        cipher_polys, n = ntruEncrypt(data, SNPK)
        # print(type(cipher_polys))
        # cipher_polys, n = ntruEncrypt(str(data), SNPK)

        sm = []
        for cipher_poly in cipher_polys:
            sm.append(cipher_poly.coeffs)

        print(f"message encrypted: {sm}")


        tmpZx = []
        for j in sm: # [[coeffs], [coeffs]]
            tmpZx.append(Zx(coeffs=j))

        plainText = ntruDecrypt(tmpZx, SNSK, n)
        
        # print(f"message decrypted: {plainText}")

        print(f"result: {plainText == data}")

        elaspsed_time = timer() - t
        eval_data = {'Method': ['NTRU'], 'PID Length': [f'{i}'],
                     'Elasped Time (sec)': [timedelta(seconds=elaspsed_time).total_seconds()]}

        print(eval_data)
        df = concatDataFrame(df, eval_data)

        # ====== Next Loop ======
        i += 1
        # data += f",PID{i}:AAAA" # `PID` must be capital for NTRU

    # print(df.head())


if __name__ == '__main__':
    main()
