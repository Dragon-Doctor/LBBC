import HashFun


class Node(object):
    def __init__(self, hashF, data, prehashed=False):
        if prehashed:
            self.val = data
        else:
            self.val = hashF.hash(data)

        self.left_child = None
        self.right_child = None
        self.parent = None
        self.bro = None
        self.side = None

    def __repr__(self):
        return "MerkleTreeNode('{0}')".format(self.val)


class MerkleTree(object):

    def __init__(self, A, B, leaves=[]):
        self.hashF = HashFun.PQHash(A, B)
        self.leaves = [Node(self.hashF, leaf, True) for leaf in leaves]
        self.root = self.get_root()

    def add_node(self, leaf):
        self.leaves.append(Node(self.hashF, leaf))

    def clear(self):
        self.root = None
        for leaf in self.leaves:
            leaf.parent, leaf.bro, leaf.side = (None,) * 3

    def get_root(self):
        if not self.leaves:
            return None

        level = self.leaves[::]
        while len(level) != 1:
            level = self._build_new_level(level)
        self.root = level[0]
        return self.root.val

    def _build_new_level(self, leaves):
        new, odd = [], None
        if len(leaves) % 2 == 1:
            odd = leaves.pop(-1)
        for i in range(0, len(leaves), 2):
            newnode = Node(self.hashF, f"{leaves[i].val}{leaves[i + 1].val}")
            newnode.lelf_child, newnode.right_child = leaves[i], leaves[i + 1]
            leaves[i].side, leaves[i + 1].side, = 'LEFT', 'RIGHT'
            leaves[i].parent, leaves[i + 1].parent = newnode, newnode
            leaves[i].bro, leaves[i + 1].bro = leaves[i + 1], leaves[i]
            new.append(newnode)
        if odd:
            new.append(odd)
        return new

    def get_path(self, index):
        path = []
        this = self.leaves[index]
        path.append((this.val, 'SELF'))
        while this.parent:
            path.append((this.bro.val, this.bro.side))
            this = this.parent
        path.append((this.val, 'ROOT'))
        return path


def get_merkle_root_of_txs(A, B, txs):
    return get_merkle_root(A, B, [tx for tx in txs])


def get_merkle_root(A, B, level):
    while len(level) != 1:
        odd = None
        if len(level) % 2 == 1:
            odd = level.pop()

        level = [HashFun.PQHash(A, B).hash(i1 + i2) for i1, i2 in pair_node(level)]

        if odd:
            level.append(odd)
    return level[0]


def pair_node(l):
    return (l[i:i + 2] for i in range(0, len(l), 2))
