import socket
import threading
from contextlib import closing
   
def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return 1
        else:
            return 0

IP = socket.gethostbyname(socket.gethostname())
PORT = 7777
while True:
    if(check_socket(IP,PORT)):
        PORT+=1
    else:
        print(PORT)
        break
ADDR = (IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)
server.listen()

clients = []
names = []
ids=[]

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client,addr):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            ids.pop(index)
            # name = names(index)
            # names.remove(name)
            broadcast(f"{names.pop(index)} left".encode('ascii'))
            break

def receive():
    while True:
        client, addr = server.accept()
        print(f"{addr} connected")

        client.send("Name".encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)
        if(ids==[]):
            client.send("ID: 0".encode('ascii'))
            id = 0
        else:
            client.send(("ID: " + str(ids[-1]+1)).encode('ascii'))
            id = ids[-1]+1
        ids.append(id)

        print(f"Name of the client is {name}")
        print(f"ID of the client is: {id}")
        broadcast(f"{name} joined".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,addr))
        thread.start()

print(f"Server is listening..")
receive()
        
