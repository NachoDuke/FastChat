import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 7777
ADDR = (IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients = []
names = []

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

        print(f"Name of the client is {name}")
        broadcast(f"{name} joined".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,addr))
        thread.start()

print(f"Server is listening..")
receive()
        
