#this is the distribution server
import socket
import threading
import time
import os

#returns the port number with the least number of devices connected to it
def portMin(loads):
    minLoad = 0
    for i in range(len(loads)):
        if loads[i]<loads[minLoad]:
            minLoad = i
    return minLoad


def receive():
    servers = []
    ports = []
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
        client, addr = server.accept()
        print(f"{addr} connected")
        #find the minimum
        min = str(ports[(portMin(loads))])
        print(min)
        loads[portMin(loads)]+=1
        client.send(min.encode('ascii'))

if __name__=="__main__":
    IP = socket.gethostbyname(socket.gethostname())
    ADDR = (IP, 0)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    PORT = server.getsockname()[1]
    with open("dsPort.txt",'w') as f:
        f.write(str(PORT))
    server.listen()
    print("Server is listening")
    receive()