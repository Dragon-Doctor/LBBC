from hashlib import sha256

import numpy as np

'''
后量子hash函数 Fun
class PQHash包括： 
压缩函数            pres_f(u0, u1)
hash函数           hash(bits)

二进制转十进制向量    b2v(bin_u)
十进制向量转为01串   Hash_root_value(hash_vector)
十进制向量转为hex串  Hash_root_16(hash_vector)

函数：
随机比特流          ran_str(num):

@Author 
E-mail:longbohan@hdu.edu.cn
'''


class PQHash(object):
    def __init__(self, A, B):
        self.n = 2 ** 8
        self.k = 8
        self.q = 2 ** 8
        self.A = A
        self.B = B
        self.nk = self.n * self.k
        # self.G = self.Gen_G()

    # 十进制向量转换为二进制向量
    def bin_trans(self, x):
        result = []
        re_sq = np.array(x).reshape(self.n)
        # 转为二进制串
        result = ''.join(['{:08b}'.format(int_item) for int_item in re_sq])
        return self.b_2_bv(result)

    # 压缩函数
    def pres_f(self, u0, u1):
        Au0 = np.dot(self.A, u0)
        Bu1 = np.dot(self.B, u1)
        u = np.mod((Au0 + Bu1), self.q)
        # 转换为nk*1的向量
        return self.bin_trans(u)

    # 转十进制向量
    def b2v(self, bin_u):
        # 计算 G*U
        return np.dot(self.G, bin_u)

    # 将01向量转为01串
    def v2b(self, hash_vector):
        return ''.join(str(bit) for bit in hash_vector.reshape(2048))

    # 将01串转为hex串
    def Hash_root_16(self, string_2):
        return hex(int(string_2, 2))[2:]

    # 将hex串转01串
    def hex_2_bin(self, string):
        return bin(int(string, 16))[2:]

    # 将01串转01向量
    def b_2_bv(self, string):
        return np.array(list(string), dtype=int).reshape(self.nk, 1)

    # 后量子的Hash函数
    def hash(self, bits):
        # 判断整除并计算多出的比特
        ext_bit = len(bits) % self.nk
        """
        last_bits = []
        # 填充比特流
        if ext_bit + 2 > self.nk:
            temp_list = [1] + [0] * (2 * self.nk - ext_bit - 2) + [1]
            last_bits.extend(list(bits))
            last_bits.extend(temp_list)
        elif ext_bit + 2 == self.nk:
            last_bits.extend(bits)
            last_bits.extend([1, 1])
        else:
            temp_list = [1] + [0] * (self.nk - ext_bit - 2) + [1]
            last_bits.extend(bits)
            last_bits.extend(temp_list)

        """
        if ext_bit + 2 > self.nk:
            temp_list = '1' + '0' * (2 * self.nk - ext_bit - 2) + '1'
            last_bits = f'{bits}{temp_list}'
        elif ext_bit + 2 == self.nk:
            temp_list = '11'
            last_bits = f'{bits}{temp_list}'
        else:
            temp_list = '1' + '0' * (self.nk - ext_bit - 2) + '1'
            last_bits = f'{bits}{temp_list}'
        last_bits = list(last_bits)

        # 将输入的比特流分块成nk*1的向量
        hash_list = np.array(last_bits, dtype=int).reshape(len(last_bits) // self.nk, self.nk)
        hash_value = np.asarray(hash_list[0]).reshape(self.nk, 1)
        # 进行迭代hash
        for item in range((len(last_bits) // self.nk) - 1):
            hash_value = self.pres_f(hash_value, np.asarray(hash_list[item + 1]).reshape(self.nk, 1))

        return self.v2b(hash_value)


# 随机比特流
def ran_str(num):
    salt_int_list = np.random.randint(2, high=None, size=num, dtype=np.int8)
    salt_str = ''.join(str(item) for item in salt_int_list)

    return salt_str


def str2int(msg):  # msg to int
    # msg_b = bytes(msg, encoding="utf8")
    # return int.from_bytes(msg_b, byteorder='big', signed=False)
    return int.from_bytes(sha256(bytes(msg, encoding='utf8')).digest(), byteorder='big', signed=False)


def quickPower(a, b, c):
    result = 1
    while b > 0:
        if b % 2 == 1:
            result = result * a % c
        a = a * a % c
        b >>= 1
    return result


def mulMatrix(x, y):  # 定义二阶矩阵相乘的函数
    ans = [[0 for i in range(2)] for j in range(2)]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                ans[i][j] += x[i][k] * y[k][j]
    return ans


def quickMatrix(m, n):
    E = [[0 for i in range(2)] for j in range(2)]  # 先定义一个单位矩阵
    for i in range(2):
        E[i][i] = 1
    while (n):
        if n % 2 != 0:
            E = mulMatrix(E, m)
        m = mulMatrix(m, m)
        n >>= 1
    return E
