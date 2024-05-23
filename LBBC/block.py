"""
区块设计
"""
import time
import hashlib


class Block:
    # 初始化一个区块
    def __init__(self, previous_hash, data):
        self.index = 0
        self.nonce = ''
        self.previous_hash = previous_hash
        self.time_stamp = time.time()
        self.data = data
        self.hash = self.get_hash()

    # 获取区块的hash
    def get_hash(self):
        msg = hashlib.sha256()
        msg.update(str(self.previous_hash).encode('utf-8'))
        msg.update(str(self.data).encode('utf-8'))
        msg.update(str(self.time_stamp).encode('utf-8'))
        msg.update(str(self.index).encode('utf-8'))
        return msg.hexdigest()

    # 修改区块的hash值
    def set_hash(self, hash):
        self.hash = hash


# 生成创世区块，这是第一个区块，没有前一个区块
def creat_genesis_block():
    block = Block(previous_hash='0000', data='Genesis block')
    nonce, digest = mime(block=block)
    block.nonce = nonce
    block.set_hash(digest)
    return block


def mime(block):
    """
    挖矿函数——更新区块结构，加入nonce值
        block:挖矿区块
    """
    i = 0
    prefix = '0000'
    while True:
        nonce = str(i)
        msg = hashlib.sha256()
        msg.update(str(block.previous_hash).encode('utf-8'))
        msg.update(str(block.data).encode('utf-8'))
        msg.update(str(block.time_stamp).encode('utf-8'))
        msg.update(str(block.index).encode('utf-8'))
        msg.update(nonce.encode('utf-8'))
        digest = msg.hexdigest()
        if digest.startswith(prefix):
            return nonce, digest
        i += 1
