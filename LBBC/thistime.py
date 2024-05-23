import time

import numpy as np


class PQHash(object):
    def __init__(self, A, B):
        self.n = 2 ** 8
        self.k = 8
        self.q = 2 ** 8
        self.A = A
        self.B = B
        self.nk = self.n * self.k
        # self.G = self.Gen_G()

    def mat_pow(self, A, n):
        m = A.shape[0]
        B = np.eye(m, dtype=np.int64)
        while n > 0:
            if (n & 1) != 0:
                B = np.mod(np.matmul(B, A), self.q).astype(np.int64)
            A = np.mod(np.matmul(A, A), self.q).astype(np.int64)
            n >>= 1
        return B

    def hex_2_bin(self, string):
        return bin(int(string, 16))[2:]


def hex_2_bin(string):
    last = ''
    for bit in string:
        last += bin(int(bit, 16))[2:].zfill(4)
    return last


a = '0'
T1 = time.time()
c = bin(int(a, 16))[2:]
d = c.zfill(4)
begin_bit = '0123456789abcdeffedcba9876543210' * 8
A = hex_2_bin(begin_bit)
time.sleep(5)
b = len(A)
T2 = time.time()
print(T2 - T1)
