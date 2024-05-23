from simchain import *
import time

net = Network()

alice = net.peers[0]
bob = net.peers[3]

text_data = []

for i in range(1, 50):
    T1 = time.time()
    net.make_random_transactions(i)
    T2 = time.time()
    net.consensus(meth=pow(0))
    T3 = time.time()
    text_data.append(f'{i} {(T2 - T1) * 1000} {(T3 - T1) * 1000}')
T4 = time.time()
print((T4 - T1))
f = open('bitcoin_test.txt', mode='w', encoding='utf-8')
f.writelines('\n'.join(text_data))
f.close()
