import numpy as np
import HashFun, time, struct, binascii

'''
后量子hash函数 Fun
包括： 
压缩函数            pres_f(q, A, B, u0, u1)
hash函数           PQhash(bits, n, k, q, A, B)

二进制转十进制向量    b2v(n, k, bin_u)
十进制向量转为01串   Hash_root_value(hash_vector)
十进制向量转为hex串  Hash_root_16(hash_vector)

随机比特流          def ran_str(num):

@Author 
longbohan@hdu.edu.cn
'''


# 转换为二进制向量
def bin_trans(x):
    result = []
    d = np.array(x).reshape(256)
    for int_item in d:
        # int_item = int_item[0]
        int_bin_str = bin(int_item)[2:]
        int_bin_list = [int(item) for item in int_bin_str]

        if len(int_bin_list) < 8:
            temp_list = [0] * (8 - len(int_bin_list))
            temp_list.extend(int_bin_list)
            result.append(temp_list)
        else:
            result.append(int_bin_list)
    result = np.array(result).reshape(2048, 1)
    return result


# 初始化G
def Gen_G(n, k):
    base1 = []
    G = []
    for base_item in range(k - 1, -1, -1):
        base1.append(2 ** base_item)

    for G_item in range(n):
        G.extend([0] * G_item * k)
        G.extend(base1)
        G.extend([0] * k * (n - G_item - 1))
    G = np.array(G).reshape(n, n * k)
    return G


# 压缩函数
def pres_f(q, A, B, u0, u1):
    Au0 = np.dot(A, u0)
    Bu1 = np.dot(B, u1)
    u = np.remainder((Au0 + Bu1), q)
    u = np.asarray(u).reshape(256)
    # 转换为nk*1的向量
    bin_u = bin_trans(u)
    return bin_u


# 转十进制向量
def b2v(G, bin_u):
    # 计算 G*U
    hash_vector = np.dot(G, bin_u)
    return hash_vector


# 将向量转为01串
def Hash_root_value(hash_vector):
    hash_list_item = []
    for item in bin_trans(hash_vector):
        hash_list_item.extend(item)
    # 转为01串
    Hash_list = ''.join(str(bit) for bit in hash_list_item)
    return Hash_list



# 将向量转为hex串
def Hash_root_16(hash_vector):
    hash_vector = hash_vector.reshape(256)
    base16 = []
    for bit in hash_vector:
        bit_hex_str = hex(bit)[2:]
        if len(bit_hex_str) < 2:
            base16.append('0')
        base16.append(bit_hex_str)
    hash_value_16 = ''.join(str(bit) for bit in base16)
    return hash_value_16


# 后量子的Hash函数
def PQhash(bits, n, k, q, A, B):
    # 检测输入的比特流的长度 并扩充到32位
    ori_str_len = []
    bin_len_b = bin(len(bits))[2:]
    bin_len_list = [int(item) for item in bin_len_b]
    if len(bin_len_list) < 32:
        temp_list1 = [0] * (32 - len(bin_len_list))
        temp_list1.extend(bin_len_list)
        ori_str_len.extend(temp_list1)
    else:
        ori_str_len.extend(bin_len_list)

    # 检测输入的比特流是否为nk的整数倍 并填充
    a = len(bits)
    # 判断整除并计算多出的比特
    ext_bit = len(bits) % (n * k)
    # more_bit = ((ext_bit + 1) * n * k) - len(bits)
    last_bits = []
    # 填充比特流
    if ext_bit + 32 > (n * k):
        temp_list = [0] * (2 * (n * k) - ext_bit - 32)
        temp_list.extend(ori_str_len)
        last_bits.extend(bits)
        temp_list_str = ''.join(str(ite) for ite in last_bits)
        last_bits.extend(temp_list_str)
    elif ext_bit + 32 == (n * k):
        last_bits.extend(bits)
        temp_list_str = ''.join(str(ite) for ite in ori_str_len)
        last_bits.extend(temp_list_str)
    else:
        temp_list = [0] * ((n * k) - ext_bit - 32)
        temp_list.extend(ori_str_len)
        last_bits.extend(bits)
        temp_list_str = ''.join(str(ite) for ite in temp_list)
        last_bits.extend(temp_list_str)

    # 将输入的比特流分块成nk*1的向量
    hash_list = np.array(last_bits, dtype=int).reshape(len(last_bits) // (n * k), (n * k))
    hash_value = np.asarray(hash_list[0]).reshape(2048, 1)
    # 进行迭代hash
    for item in range((len(last_bits) // (n * k)) - 1):
        nex_p = np.asarray(hash_list[item + 1]).reshape(2048, 1)
        hash_value = pres_f(q, A, B, hash_value, nex_p)
    # hash_value.extend(Mid_p)
    return hash_value


# 随机比特流
def ran_str(num):
    salt_int_list = np.random.randint(2, high=None, size=num, dtype=np.int8)
    salt_str = ''.join(str(num) for num in salt_int_list)

    return salt_str


np.random.seed(1)
d, n, m, k, q = 2 ** 8, 2 ** 8, 2 ** 12, 8, 2 ** 8
A = np.random.randint(0, d + 1, (n, n * k))
B = np.random.randint(0, d + 1, (n, n * k))
bits = ran_str(5000)
Hash1 = HashFun.PQHash(A, B)
T1 = time.time()
f = len(Hash1.hash(bits))
T2 = time.time()
print('程序运行时间:%s毫秒' % ((T2 - T1) * 1000))
print(1)
