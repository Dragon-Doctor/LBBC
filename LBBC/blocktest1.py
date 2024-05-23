from BLockChain import *

# 创建一个区块链
bc = BlockChain()
# 添加区块
bc.add_block(data='second block')
bc.add_block(data='third block')
bc.add_block(data='fourth block')
for bl in bc.blocks:
    print("Index:{}".format(bl.index))
    print("Nonce:{}".format(bl.nonce))
    print("Hash:{}".format(bl.hash))
    print("Pre_Hash:{}".format(bl.previous_hash))
    print("Time:{}".format(bl.time_stamp))
    print("Data:{}".format(bl.data))
    print('\n')
