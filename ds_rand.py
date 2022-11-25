#this is the distribution server
import socket
import threading
import time
import os
from cryptography.fernet import Fernet
import random


servers = []
ports = []
loads = []

#returns the port number with the least number of devices connected to it
def getServer():
    return random.randint(0,len(servers)-1)

def route():
    global loads
    #Load up the servers list
    with open("port.txt",'r') as f:
        s = f.readlines()
        i=0
        for serv in s:
            servers.append(i)
            ports.append(int(serv))
            i+=1
    print(servers)
    print(ports)
    loads = [0 for i in range(len(servers))]
    while True:
        try:
            client, addr = server.accept()
            print(f"{addr} connected")
            msg = client.recv(1024).decode()
            if msg == "route":
                #find the minimum
                index = getServer()
                min = str(ports[index])
                print(min)
                loads[index]+=1
                client.send(min.encode())
            else:
                port = int(msg)
                index = ports.index(port)
                loads[index]-=1
        except Exception as e:
            print(e)
            continue

if __name__=="__main__":
    key = Fernet.generate_key()
    fernetFile = "pkeys/fernet.key"
    with open (fernetFile,"wb") as f:
        f.write(key)
    IP = socket.gethostbyname(socket.gethostname())
    ADDR = (IP, 0)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    PORT = server.getsockname()[1]
    with open("dsPort.txt",'w') as f:
        f.write(str(PORT))
    server.listen()
    print("Server is listening")
    route()