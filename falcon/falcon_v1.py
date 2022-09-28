# from numpy import set_printoptions
# from math import sqrt

# # https://pycryptodome.readthedocs.io/en/latest/src/hash/shake256.html
# # pip3 install pycryptodome
# from Crypto.Hash import SHAKE256

# # Randomness
# from os import urandom

# from .common import q
# from .fft import fft, ifft, sub, neg, add_fft, mul_fft
# from .ntt import sub_zq, mul_zq, div_zq
# from .ffsampling import gram, ffldl_fft, ffsampling_fft
# from .ntrugen import ntru_gen, ntru_solve
# from .encoding import compress, decompress
# from .rng import ChaCha20

# # For debugging purposes
# import sys
# if sys.version_info >= (3, 4):
#     from importlib import reload  # Python 3.4+ only.


# logn = {
#     2: 1,
#     4: 2,
#     8: 3,
#     16: 4,
#     32: 5,
#     64: 6,
#     128: 7,
#     256: 8,
#     512: 9,
#     1024: 10
# }


# # Bytelength of the signing salt and header
# HEAD_LEN = 1
# SALT_LEN = 40
# SEED_LEN = 56


# # Parameter sets for Falcon:
# # - n is the dimension/degree of the cyclotomic ring
# # - sigma is the std. dev. of signatures (Gaussians over a lattice)
# # - sigmin is a lower bounds on the std. dev. of each Gaussian over Z
# # - sigbound is the upper bound on ||s0||^2 + ||s1||^2
# # - sig_bytelen is the bytelength of signatures
# Params = {
#     # FalconParam(2, 2)
#     2: {
#         "n": 2,
#         "sigma": 144.81253976308423,
#         "sigmin": 1.1165085072329104,
#         "sig_bound": 101498,
#         "sig_bytelen": 44,
#     },
#     # FalconParam(4, 2)
#     4: {
#         "n": 4,
#         "sigma": 146.83798833523608,
#         "sigmin": 1.1321247692325274,
#         "sig_bound": 208714,
#         "sig_bytelen": 47,
#     },
#     # FalconParam(8, 2)
#     8: {
#         "n": 8,
#         "sigma": 148.83587593064718,
#         "sigmin": 1.147528535373367,
#         "sig_bound": 428865,
#         "sig_bytelen": 52,
#     },
#     # FalconParam(16, 4)
#     16: {
#         "n": 16,
#         "sigma": 151.78340713845503,
#         "sigmin": 1.170254078853483,
#         "sig_bound": 892039,
#         "sig_bytelen": 63,
#     },
#     # FalconParam(32, 8)
#     32: {
#         "n": 32,
#         "sigma": 154.6747794602761,
#         "sigmin": 1.1925466358390344,
#         "sig_bound": 1852696,
#         "sig_bytelen": 82,
#     },
#     # FalconParam(64, 16)
#     64: {
#         "n": 64,
#         "sigma": 157.51308555044122,
#         "sigmin": 1.2144300507766141,
#         "sig_bound": 3842630,
#         "sig_bytelen": 122,
#     },
#     # FalconParam(128, 32)
#     128: {
#         "n": 128,
#         "sigma": 160.30114421975344,
#         "sigmin": 1.235926056771981,
#         "sig_bound": 7959734,
#         "sig_bytelen": 200,
#     },
#     # FalconParam(256, 64)
#     256: {
#         "n": 256,
#         "sigma": 163.04153322607107,
#         "sigmin": 1.2570545284063217,
#         "sig_bound": 16468416,
#         "sig_bytelen": 356,
#     },
#     # FalconParam(512, 128)
#     512: {
#         "n": 512,
#         "sigma": 165.7366171829776,
#         "sigmin": 1.2778336969128337,
#         "sig_bound": 34034726,
#         "sig_bytelen": 666,
#     },
#     # FalconParam(1024, 256)
#     1024: {
#         "n": 1024,
#         "sigma": 168.38857144654395,
#         "sigmin": 1.298280334344292,
#         "sig_bound": 70265242,
#         "sig_bytelen": 1280,
#     },
# }


# # f = [4, 6, 4, -4, 5, -2, -2, 0, 1, -8, -2, 3, 3, -8, 6, 3, 0, 2, -4, 0, -5, 1, 1, 3, -1, -2, -3, -9, -4, 1, 3, 1, -3, 2, -4, 5, -6, 2, 3, -3, -9, -3, -1, -6, -5, -2, -2, 2, 4, -6, -3, 5, 0, 1, 1, 5, -2, 0, 1, 2, -3, 1, 9, 8, -1, -3, 0, -3, -2, 1, 1, 1, 0, 2, 4, 1, 0, 3, -7, 3, -4, 3, 3, -1, 3, -1, -9, -5, 6, 4, 3, 6, 5, 8, 6, 1, 2, -4, 4, 3, -3, 2, 2, 0, 1, 1, -4, 2, 5, 5, 0, 5, 0, 3, -11, -5, 1, 3, -10, -1, -6, 3, 0, -3, -4, 2, -8, 1, -4, 8, -3, -1, 5, -3, 4, 2, -3, -1, 0, -4, -2, -4, 5, 3, 7, -1, 10, 5, -5, 4, 2, 4, 1, 2, -2, -4, 1, 4, 1, 3, -6, -4, 1, 1, 1, 3, 0, -6, 3, 6, 1, -10, -2, -1, 1, -3, 1, 1, 7, -8, -2, 1, 7, -1, 3, 1, 0, 0, -6, -1, -3, 2, 0, 5, 1, 2, -4, 0, 0, 3, -10, -1, 4, -5, -4, -2, -5, -7, 5, -1, 2, 8, 4, -3, -5, -4, 0, 0, -3, 1, -5, 4, -4, 1, 0, -7, -8, 4, -5, -1, 4, 6, -4, 2, 5, 6, 7, 3, -4, -4, 4, -1, -4, 8, -3, 0, 6, 1, -9, -2, -2, -7, 7, -5, -3, -
# #      5, -3, 0, -3, -2, 1, 1, -5, 3, -3, -9, 1, 1, -3, -4, 1, -7, -1, -5, -5, 1, 2, -1, 4, 2, 2, -1, 2, 1, 3, -7, -3, 3, 0, 1, 7, -7, -5, -6, -4, 4, 0, -3, -2, -2, 1, 3, -3, 1, 3, 3, 6, 3, -4, 2, 7, 5, -2, 2, 1, 1, -2, 0, 1, 1, 2, 1, -2, 6, -1, 8, -5, -5, 4, -3, 5, 5, 2, 3, -7, 4, -1, -2, -1, 1, 0, 3, 1, -1, 4, -1, -2, -3, 1, -2, 2, -6, -4, 1, 3, -1, -5, -4, 0, 0, -3, 7, 0, -3, 1, 0, -2, 1, -1, -4, 7, -3, -1, -3, 4, 7, -1, -7, -4, 2, 3, -4, 2, 2, 3, 3, 9, 1, -1, -6, 1, -4, 0, 0, 2, 1, 3, 1, -4, 6, -2, 4, -5, -1, -1, 1, -2, -2, -7, -1, 2, -4, -4, 0, 5, 1, -1, 2, -2, 3, -4, 4, 1, -2, -2, 2, 4, -3, -2, 2, 3, -4, 4, 3, 0, -1, 0, 0, 7, 7, 5, 2, 5, -5, -2, -4, 4, 7, 0, -6, -6, -5, 2, 0, 2, 4, 1, -1, 3, -4, -2, -4, -3, 5, 0, -9, 1, 5, 2, -5, -4, 4, -1, -1, -3, 4, 1, 4, 6, 1, -2, 3, 4, 4, -3, -1, -1, 0, -2, 4, 0, 4, 0, -2, 8, -2, -8, 0, 4, -2, 0, 5, 7, -3, -4, -7, -1, -1, -3, -2, -5, -1]
# # g = [1, 2, -8, 5, -3, -3, 0, 2, 4, -1, 1, -3, 4, 2, -3, 3, 0, 4, 0, -2, -4, 5, 7, 3, -1, -1, -5, -5, -6, -4, 6, 3, 5, 0, -6, -2, -2, 4, -4, -7, 3, -2, 1, 2, 4, -3, 1, 0, 0, -5, 1, -4, 3, -3, 1, 5, -5, 2, 2, 7, 4, -6, 1, -3, 1, 1, 7, 4, 7, 5, -2, 5, -8, 2, -6, 4, -5, -14, -1, -1, 5, 7, -4, -2, -2, -1, 1, 1, -6, -3, 5, 4, 6, 5, 0, 0, -2, -3, 0, -10, -1, -7, -9, -3, -1, -6, -2, -1, 0, 4, -4, 5, 5, 7, -5, 6, 1, 0, 8, -3, -4, -3, 1, 6, 4, 3, 2, -3, 0, -6, -6, 3, 4, -3, 11, -4, 3, -4, 5, -3, 1, -1, -4, 5, 9, -2, -8, 6, 3, 4, -8, -4, -3, 2, -1, 1, -7, -2, 2, 0, 5, -4, -2, 8, 1, -1, -2, 1, -6, -1, -6, -3, 2, -1, -2, -6, -6, 0, 1, 3, 4, 0, -4, -4, 2, 1, 6, -2, 3, 1, 1, -1, -1, -8, 8, 0, 3, 1, -8, -2, -7, -6, 4, 1, -9, -1, -7, 4, 0, -3, 3, 5, 2, -2, 2, -5, 8, -3, -6, 1, -2, -1, 2, -6, -2, -5, -4, -9, 4, 0, -2, 1, -8, -2, 3, 3, 2, -7, 1, 3, -8, -4, -3, 0, -2, -7, 3, 8, 1, 3, -2, 1, 5, 3, 2, -3, -1,
# #      6, -6, 4, 3, -4, -6, -1, 11, 0, -1, -2, 5, 3, -1, 0, -8, 3, 3, 1, -3, 6, 2, 1, 3, -6, -7, 10, -2, -3, -3, -1, 1, 2, -3, 1, -4, 4, 4, -8, -5, 0, -2, -4, 6, -1, -1, -10, -1, 6, -2, 1, -2, -2, -4, -4, 0, 2, -2, -6, -1, -5, 1, -3, 6, -1, 1, -3, 1, -6, -1, -3, -7, -2, 0, -3, 3, 4, 0, 4, 1, 3, -2, 4, 4, -4, -2, 1, 3, -4, 6, -3, 4, -7, -1, -3, -2, 1, 6, -6, 5, 3, -2, 4, 1, -4, -6, -3, 0, -14, 3, 7, 0, -2, 1, 1, 8, -3, -2, -6, 4, -3, -4, 2, 2, -1, -4, 1, 2, 6, 1, -2, -8, -1, 3, 3, -5, 8, 8, 2, 3, -5, -5, -3, -1, -5, 5, -6, 0, -4, 7, -3, -3, -2, -1, -3, 6, 7, -4, 4, 3, -4, 7, 1, -1, -4, 0, 1, 6, 2, -3, 1, -6, -1, 0, -5, 5, -6, 2, 3, 1, -4, 3, -4, -1, 0, -7, 5, -8, -6, -3, -2, -5, -11, -7, -4, -4, 4, 2, 1, 5, 3, -7, -4, 2, -1, 1, 9, 5, 4, -6, -1, -3, 0, -2, 0, -1, -4, -4, 5, -4, 0, -3, 0, 11, 3, 2, -5, 2, -3, -6, 3, -2, -5, 1, -2, 4, -1, 1, -3, 3, -1, -1, -1, -2, -2, -2, -1, -8, 2, -4, 6, 0, -6, 3, 2]


# def print_tree(tree, pref=""):
#     # print(f"print_tree tree : {tree}")
#     """
#     Display a LDL tree in a readable form.

#     Args:
#         T: a LDL tree

#     Format: coefficient or fft
#     """
#     leaf = "|_____> "
#     top = "|_______"
#     son1 = "|       "
#     son2 = "        "
#     width = len(top)

#     a = ""
#     if len(tree) == 3:
#         if (pref == ""):
#             a += pref + str(tree[0]) + "\n"
#         else:
#             a += pref[:-width] + top + str(tree[0]) + "\n"
#         a += print_tree(tree[1], pref + son1)
#         a += print_tree(tree[2], pref + son2)
#         return a

#     else:
#         return (pref[:-width] + leaf + str(tree) + "\n")


# def normalize_tree(tree, sigma):
#     # print(f"normalize_tree tree : {tree}")
#     # print(f"normalize_tree sigma : {sigma}")
#     """
#     Normalize leaves of a LDL tree (from values ||b_i||**2 to sigma/||b_i||).

#     Args:
#         T: a LDL tree
#         sigma: a standard deviation

#     Format: coefficient or fft
#     """
#     if len(tree) == 3:
#         normalize_tree(tree[1], sigma)
#         normalize_tree(tree[2], sigma)
#     else:
#         tree[0] = sigma / sqrt(tree[0].real)
#         tree[1] = 0


# def sample_preimage(n, f, g, point, seed=None):

#     sigmin = Params[n]["sigmin"]
    
#     F, G = genFG(f, g)
#     B0 = [[g, neg(f)], [G, neg(F)]]
#     G0 = gram(B0)
#     G0_fft = [[fft(elt) for elt in row] for row in G0]

#     [[a, b], [c, d]] = [[fft(elt) for elt in row] for row in B0]

#     point_fft = fft(point)
#     t0_fft = [(point_fft[i] * d[i]) / q for i in range(n)]
#     t1_fft = [(-point_fft[i] * b[i]) / q for i in range(n)]
#     t_fft = [t0_fft, t1_fft]
#     T_fft = ffldl_fft(G0_fft)

#     if seed is None:
#         # If no seed is defined, use urandom as the pseudo-random source.
#         z_fft = ffsampling_fft(t_fft, T_fft, sigmin, urandom)
#         # print(f"sample_preimage z_fft : \n{z_fft}\n")
#     else:
#         # If a seed is defined, initialize a ChaCha20 PRG
#         # that is used to generate pseudo-randomness.
#         chacha_prng = ChaCha20(seed)
#         z_fft = ffsampling_fft(t_fft, T_fft, sigmin,
#                                chacha_prng.randombytes)

#     v0_fft = add_fft(mul_fft(z_fft[0], a), mul_fft(z_fft[1], c))
#     v1_fft = add_fft(mul_fft(z_fft[0], b), mul_fft(z_fft[1], d))
#     v0 = [int(round(elt)) for elt in ifft(v0_fft)]
#     v1 = [int(round(elt)) for elt in ifft(v1_fft)]

#     s = [sub(point, v0), neg(v1)]
#     # print(f"sample_preimage s : \n{s}\n")
#     # print(f"sample_preimage len(s[0]) : \n{len(s[0])}\n")
#     return s


# def hash_to_point(n, message, salt):

#     if q > (1 << 16):
#         raise ValueError("The modulus is too large")

#     k = (1 << 16) // q
#     # Create a SHAKE object and hash the salt and message.
#     shake = SHAKE256.new()
#     shake.update(salt)
#     shake.update(message)
#     # Output pseudorandom bytes and map them to coefficients.
#     hashed = [0 for i in range(n)]
#     i = 0
#     j = 0
#     while i < n:
#         # Takes 2 bytes, transform them in a 16 bits integer
#         twobytes = shake.read(2)
#         elt = (twobytes[0] << 8) + twobytes[1]  # This breaks in Python 2.x
#         # Implicit rejection sampling
#         if elt < k * q:
#             hashed[i] = elt % q
#             i += 1
#         j += 1
#     return hashed


# def genFG(f, g):
#     F, G = ntru_solve(f, g)
#     F = [int(coef) for coef in F]
#     G = [int(coef) for coef in G]
#     return F, G


# def genFPK(n, f, g):

#     sigma = Params[n]["sigma"]

#     # f, g, F, G = ntru_gen(n)
#     F, G = genFG(f, g)
#     B0 = [[g, neg(f)], [G, neg(F)]]
#     G0 = gram(B0)
#     B0_fft = [[fft(elt) for elt in row] for row in B0]
#     G0_fft = [[fft(elt) for elt in row] for row in G0]
#     T_fft = ffldl_fft(G0_fft)

#     normalize_tree(T_fft, sigma)

#     # Public Key
#     h = div_zq(g, f)
#     # print(f"h: {h}\n")

#     # Private Key -> f,g
#     # print(f"f: {f}\n\ng: {g}\n\nF: {F}\n\nG: {G}")
#     # print(
#     #     f"len : \nh = {len(h)}\nf = {len(f)}\ng = {len(g)}\nF = {len(F)}\nG = {len(G)}")

#     return h


# def sign(n, f, g, message, randombytes=urandom):
#     signature_bound = Params[n]["sig_bound"]
#     sig_bytelen = Params[n]["sig_bytelen"]

#     int_header = 0x30 + logn[n]
#     header = int_header.to_bytes(1, "little")
#     salt = randombytes(SALT_LEN)
#     # print(f"salt : {salt}")
#     hashed = hash_to_point(n, message, salt)
#     while(1):
#         # print(f"sign while loop")
#         if (randombytes == urandom):
#             # print(f"sign while loop randombytes == urandom")
#             s = sample_preimage(n, f, g, hashed)
#         else:
#             seed = randombytes(SEED_LEN)
#             s = sample_preimage(n, f, g, hashed, seed=seed)
#         norm_sign = sum(coef ** 2 for coef in s[0])
#         norm_sign += sum(coef ** 2 for coef in s[1])
#         # Check the Euclidean norm
#         if norm_sign <= signature_bound:
#             enc_s = compress(s[1], sig_bytelen - HEAD_LEN - SALT_LEN)
#             # Check that the encoding is valid (sometimes it fails)
#             if (enc_s is not False):
#                 return header + salt + enc_s


# def valid(n, h, message, signature):

#     signature_bound = Params[n]["sig_bound"]
#     sig_bytelen = Params[n]["sig_bytelen"]

#     salt = signature[HEAD_LEN:HEAD_LEN + SALT_LEN]
#     enc_s = signature[HEAD_LEN + SALT_LEN:]
#     s1 = decompress(enc_s, sig_bytelen - HEAD_LEN - SALT_LEN, n)

#     # Check that the encoding is valid
#     if (s1 is False):
#         print("Invalid encoding")
#         return False

#     # Compute s0 and normalize its coefficients in (-q/2, q/2]
#     hashed = hash_to_point(message, salt)
#     s0 = sub_zq(hashed, mul_zq(s1, h))
#     s0 = [(coef + (q >> 1)) % q - (q >> 1) for coef in s0]

#     # Check that the (s0, s1) is short
#     norm_sign = sum(coef ** 2 for coef in s0)
#     norm_sign += sum(coef ** 2 for coef in s1)
#     if norm_sign > signature_bound:
#         print("Squared norm of signature is too large:", norm_sign)
#         return False
#     # If all checks are passed, accept
#     return True
