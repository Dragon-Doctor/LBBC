from LBBC.MerkleTree import *
import time
import HashFun
import Fun

import numpy as np

np.random.seed(1)
d, n, m, k, q = 2 ** 8, 2 ** 8, 2 ** 12, 8, 2 ** 8


# 交易大小为5K+N x 5K
def ran_txs(num, size):
    txs = []
    for item in range(num):
        txs.append(HashFun.ran_str(size))
    return txs


def ran_test():
    A = np.random.randint(0, d + 1, (n, n * k))
    B = np.random.randint(0, d + 1, (n, n * k))
    return HashFun.PQHash(A, B).hash(HashFun.ran_str(4000))


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


def b2v(bin_u):
    # 计算 G*U
    G = Gen_G(2 ** 8, 8)
    return np.dot(G, bin_u)


def block(times, size):
    txs = ran_txs(2 ** times, size)
    T1 = time.time()
    A = np.random.randint(0, d + 1, (n, n * k))
    B = np.random.randint(0, d + 1, (n, n * k))
    #   hash1 = HashFun.PQHash(A, B)
    print(A, B)
    # 生成MerkleTree
    T2 = time.time()
    merkle = MerkleTree(A, B, txs)
    # merkle.root = merkle.get_root()
    T3 = time.time()
    # merkle.root = a
    # PRNG的随机种子输入
    print(hex(int(merkle.root, 2)))
    # hex(int(string_2, 2))[2:]
    random_seed = b2v(np.array([str_item for str_item in merkle.root], dtype=int).reshape(n * k, 1))

    np.random.seed(random_seed)
    T4 = time.time()
    print('MeikeTree生成时间:%s毫秒' % ((T3 - T2) * 1000))
    print('相邻区块总生成时间:%s毫秒' % ((T4 - T1) * 1000))
    print('PRNG的生成时间:%s毫秒' % ((T2 - T1 + T4 - T3) * 1000))
    return (T3 - T2) * 1000


# block generation test
test_data_list = []
for level in range(8, 9):
    for ext in range(5):
        print('----------------------------------')
        print(f'level={level} block编号= {ext} ')
        test_data_list.append(f'{level},{ext},{block(level, 1000)}')
f = open('generation.txt', mode='w', encoding='utf-8')
f.writelines('\n'.join(test_data_list))
f.close()

'''
# output the text bit string of NIST randomness test
f = open('test1.txt', mode='w', encoding='utf-8')
test_bit = []
for times in range(2000):
    test_bit.append(ran_test())
x = ''.join(test_bit)
f.write(x)
f.close()
'''
