#this is the distribution server
import socket
import threading
import time

#returns the port number with the least number of devices connected to it
def portMin(loads):
    minLoad = loads[0]
    for i in range(len(loads)):
        if loads[i]<minLoad:
            minLoad = i
    return minLoad


def receive():
    servers = []
    ports = []
    #Load up the servers list
    with open("port.txt",'r') as f:
        s = f.readlines()
        i=0
        for server in s:
            servers.append(i)
            ports.append(int(server))
            i+=1
    print(servers)
    print(ports)
    loads = [0 for i in range(len(servers))]
    while True:
        client, addr = server.accept()
        print(f"{addr} connected")
        #find the minimum
        min = str(ports[(portMin(loads))])
        client.send(min.encode('ascii'))

if _name=="main_":
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