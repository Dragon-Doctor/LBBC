from block import *


# 区块链
class BlockChain:
    def __init__(self):
        self.blocks = [creat_genesis_block()]

    # 添加区块到区块链上
    def add_block(self, data):
        pre_block = self.blocks[len(self.blocks) - 1]
        new_block = Block(pre_block.hash, data)
        new_block.index = len(self.blocks)
        nonce, digest = mime(block=new_block)
        new_block.nonce = nonce
        new_block.set_hash(digest)
        self.blocks.append(new_block)
        return new_block
