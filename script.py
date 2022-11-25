from pwn import process
import math
import random
import os
import datetime
import time

NUM = 10

p = []

for i in range(NUM):
    p.append(process(['python3','./client2.py']))
    p[i].sendline(b'2')
    p[i].sendline(str(i).encode('utf-8'))
    p[i].sendline(str(i).encode('utf-8'))
    time.sleep(0.5)

p[0].sendline(b'4')
p[0].sendline("ssl".encode())
p[0].sendline("ssl".encode())
time.sleep(0.5)

for i in range(1,NUM):
    p[i].sendline(b'5')
    p[i].sendline("ssl".encode())
    p[i].sendline("ssl".encode())
    time.sleep(0.5)

for i in range(NUM):
    p[i].sendline(b'2')
    p[i].sendline("ssl".encode())
    time.sleep(0.5)

for j in range(3):
    for i in range(NUM):
        p[i].sendline(("hello"+str(j)).encode('utf-8'))
        time.sleep(0.25)
    time.sleep(0.5)

for j in range(2):
    p[i].sendline(("/quit").encode('utf-8'))
    time.sleep(1)

for i in range(2):
    p[i].sendline(str(3).encode('utf-8'))
    p[i].sendline(str(3).encode('utf-8'))
    time.sleep(0.5)
    
    
time.sleep(5)
print('reached')
