import hashlib
import time

msg = hashlib.sha256()
value = '2' * 2 ** 12
T1 = time.time()
for i in range(6, 9):
    for j in range(2**i):
        msg.update(str(value).encode('utf-8'))
    T2 = time.time()
    print((T2 - T1)* 1000)


