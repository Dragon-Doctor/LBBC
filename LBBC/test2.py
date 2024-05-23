import time
import numpy as np

import merkle2 as mk


# 随机比特流
def ran_str(num):
    salt_int_list = np.random.randint(2, high=None, size=num, dtype=np.int8)
    salt_str = ''.join(str(item) for item in salt_int_list)
    return salt_str


# 随机交易
def ran_txs(num):
    txs = []
    for item in range(num):
        txs.append(ran_str(5000).encode('utf-8'))
    return txs


# 生成MerkleTree
def block(times):
    txs = ran_txs(2 ** times)
    T1 = time.time()
    mk1 = mk.MerkleTree(txs)
    mk1.get_root()
    T2 = time.time()
    print('MeikeTree生成时间:%s毫秒' % ((T2 - T1) * 1000))
    return (T2 - T1) * 1000


test_data_list = []
for level in range(6, 10):
    for ext in range(20):
        print('----------------------------------')
        print(f' block编号= {ext}')
        test_data_list.append(f'{block(level)} {level} {ext}')
f = open('test_sha3_256.txt', mode='w', encoding='utf-8')
f.writelines('\n'.join(test_data_list))
f.close()

