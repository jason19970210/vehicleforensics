import sys
# import time
# from datetime import timedelta
# from timeit import default_timer as timer
# import pandas as pd

import numpy as np

# add utils folder to sys path
from pathlib import Path
sys.path.append(Path(__file__).parents[2].as_posix())

# from utils.kyber_utils.ccakem import kem_keygen512, kem_encaps512, kem_decaps512
from utils.kyber_utils.cpake import generate_kyber_keys, encrypt, decrypt
import kyber_config as kconfig

def main():

    # sk, pk = kem_keygen512()
    # secret1, cipher = kem_encaps512(pub)
    # secret2 = kem_decaps512(priv, cipher)

    # print(f"{sk=}\n\n{pk=}\n\n{secret1=}\n\n{cipher=}\n\n{secret2=}")

    sk, pk = generate_kyber_keys(params_k=kconfig.generate_key_in_paramk)
    # m = [10, 85, -92, 67, 61, -70, -84, 59, 97, 109, 108, 67, 56, -4, -82, -60, -87, 104, 94, -118, -93, 125, 106, 91, -41, 77, 97, -108, -107, -51, 63, 20]
    # coins = [-128, 53, 8, -15, -92, -21, -89, 117, -36, 93, 90, -21, 102, 29, -69, -108, -42, -120, -7, 78, -58, 19, 127, -62, 65, 72, 70, 45, 35, 37, 39, 20]
    # cipher = encrypt(m=m, pubkey=pk, coins=coins, params_k=kconfig.generate_key_in_paramk)
    # m2 = decrypt(packed_ciphertext=cipher, private_key=sk, params_k=kconfig.generate_key_in_paramk)

    # print(f"{cipher=}\n\n{m2=}")

    min = 0
    max = 20
    for i in range(1, 51):
        m1 = np.random.randint(min, max, i).tolist()
        coins = np.random.randint(min, max, i).tolist()

        try:
            m2 = decrypt(packed_ciphertext=encrypt(m=m1, pubkey=pk, coins=coins, params_k=kconfig.generate_key_in_paramk), private_key=sk, params_k=kconfig.generate_key_in_paramk)
            if m1 == m2:
                print(f"{i=} success")
            else:
                print(f"{i=} failed")
                print(f"{m1=}\n\n{coins=}\n\n{m2=}")
        except Exception as e:
            print(f"{i=} error: {e}")
            continue

    
if __name__ == '__main__':
    main()