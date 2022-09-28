# Consumer
# SNSK -> SN_f, SN_g
# CFPK -> CF_h
# SFSK -> SF_f, SF_g

# Producer
# CFSK -> CF_f, CF_g
# SNPK -> SN_h

MQIP = '120.126.18.131'
MQ_USERNAME = "admin"
MQ_PWD = "admin"
MQ_QUEUE = 'DEMO'

HASH_SALT = b'$\xee\xde#\r\x07\xe8\xd3R\xe06.\x98\xf9\x0c\xb1\xa8\xa1\xaa\x06.\x00{2h2\xa6\xa6\xd9\xf3<\xc9'

N_P = 3
N_Q = 128
N_D = 5
N_elliptic_a = 7
N_elliptic_b = 5
N_N = 13

N_F = [1, -1, 0, 0, 0, -1, 0, 0, 1, 0, 1, 0, 0]
N_g = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, -1, 0]
N_h = [22, -39, -35, 62, 14, 24, 62, -19, 42, 32, -56, -20, -18, -62]

F_N = 16

F_f = [-26, 8, 9, -23, -28, -26, -33, 20, 27, -26, 11, -14, -7, -24, -19, -4]
F_g = [-4, -2, -30, 20, 59, 5, 1, 24, 3, -14, 17, -30, 11, 16, 48, 3]
F_h = [11486, 6619, 268, 1695, 1416, 6152, 11034, 2870, 4280, 8588, 6543, 7450, 2052, 2335, 6122, 158]