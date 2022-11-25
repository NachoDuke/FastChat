from pwn import process
import math
import random
import os
import datetime
import time

p = []

for i in range(2):
    p.append(process(['python3','./client.py']))
    p[i].sendline(b'2')
    p[i].sendline(str(i).encode('utf-8'))
    p[i].sendline(str(i).encode('utf-8'))
    p[i].sendline(b'1')

p[0].sendline(b'1')
p[1].sendline(b'0')
p[0].sendline("hello".encode('utf-8'))
    
    
time.sleep(5)
print('reached')