import time
from datetime import timedelta
from timeit import default_timer as timer
import pandas as pd
from hashlib import sha3_256

from falcon_utils import falcon
import falcon_config as fconfig

from ntru_utils.NtruEncrypt import *
from ntru_utils.Polynomial import Zx
from ntru_utils.num_to_polynomial import *
import ntru_config as nconfig


# Falcon Public Param.
# CFSK_N = config.F_N

# Falcon Secret Param. aka Secret Key
CFSK_f = fconfig.F_f
CFSK_g = fconfig.F_g
CFSK = falcon.SecretKey(fconfig.F_N, CFSK_f, CFSK_g)

# Falcon Public Key
CFPK = falcon.PublicKey(fconfig.F_N, CFSK.h)


# NTRU
SNPK, SNSK = generate_keypair(
    nconfig.N_P, nconfig.N_Q, nconfig.N_D, nconfig.N_N)

TEST_N = 2


def concatDataFrame(df, data):
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    return df


def ntruTrans(message):
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

    m_str = f"{time.time()}"

    i = 0

    df = pd.DataFrame(columns=['Method', 'PID Length', 'Elasped Time'])

    while i < TEST_N:

        m_byt = m_str.encode()

        # hash
        h_o = sha3_256()
        t = timer()
        h_o.update(m_byt)
        hash_elapsed_time = timer() - t
        h_byt = h_o.digest()

        # sign
        t = timer()
        s_byt = CFSK.sign(h_byt)
        sign_elapsed_time = timer() - t

        # encrypt
        # print(m_str)
        t = timer()
        e_polys, e_n = ntruEncrypt(m_str, SNPK)
        encrypt_elapsed_time = timer() - t

        e_list = []
        for e_poly in e_polys:
            e_list.append(e_poly.coeffs)

        # print(e_n) # 14

        # decrypt
        t = timer()
        d_str = ntruDecrypt(e_polys, SNSK, e_n)
        decrypt_elapsed_time = timer() - t

        # valid
        # print(d_str == m_str)

        t = timer()
        v_bool = CFPK.verify(h_byt, s_byt)
        verify_elapsed_time = timer() - t
        # print(v_bool)

        # timedelta(seconds=elaspsed_time).total_seconds
        # print(f"{i}, {timedelta(seconds=hash_elapsed_time).total_seconds()}, {timedelta(seconds=sign_elapsed_time).total_seconds()}, {timedelta(seconds=encrypt_elapsed_time).total_seconds()}, {timedelta(seconds=decrypt_elapsed_time).total_seconds()}, {timedelta(seconds=verify_elapsed_time).total_seconds()}")

        print(f"message: {m_str}\nhashed: {h_byt}\nsigned: {s_byt}\nencrypted: {e_list}\ndecrypted: {d_str}\nverified: {v_bool}")


        elaspsed_time = [timedelta(seconds=hash_elapsed_time).total_seconds(), timedelta(seconds=sign_elapsed_time).total_seconds(), 
                timedelta(seconds=encrypt_elapsed_time).total_seconds(), timedelta(seconds=decrypt_elapsed_time).total_seconds(), timedelta(seconds=verify_elapsed_time).total_seconds()]
        eval_data = {'Method': ['Full'], 
                     'PID Length': [f'{i}'],
                     'Elasped Time': [elaspsed_time[0]+elaspsed_time[1]+elaspsed_time[2]+elaspsed_time[3]+elaspsed_time[4]],
                     'Hash Elapsed': [elaspsed_time[0]],
                     'Sign Elapsed': [elaspsed_time[1]],
                     'Encr Elapsed': [elaspsed_time[2]],
                     'Decr Elapsed': [elaspsed_time[3]],
                     'Veri Elapsed': [elaspsed_time[4]],
                    }

        df = concatDataFrame(df, eval_data)

        # ====== Next Loop ======
        i += 1
        m_str += f",PID{i}:AAAA"  # `PID` must be capital for NTRU

    print(df.tail())
    df.to_csv('full_n100_server.csv', index=False)

if __name__ == '__main__':
    main()
