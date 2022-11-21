import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, 0)
QUIT = "!quit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
PORT = server.getsockname()[1]

with open("port.txt",'w') as f:
    f.write(str(PORT))

server.listen()

clients = []
names = []
login = {}

def broadcast(msg, client):
    for c in clients:
        if c == client:
            continue
        if c.fileno() != -1:
            c.send(f'{msg}'.encode('ascii'))

def handle(client,addr):
    while True:
        try:
            msg = client.recv(2048).decode('ascii')
            if msg.split(": ",1)[1] == QUIT:
                # index = clients.index(client)
                # clients.remove(client)
                client.close()
                broadcast(f"{names[index]} left",None)
                break    
            else:
                broadcast(msg,client)
        except:
            index = clients.index(client)
            # clients.remove(client)
            client.close()
            # name = names(index)
            # names.remove(name)
            broadcast(f"{names[index]} left",None)
            break

def receive():
    while True:
        client, addr = server.accept()
        print(f"{addr} connected")

        client.send("entry_type".encode('ascii'))
        entry = client.recv(1024).decode('ascii')
        name = client.recv(1024).decode('ascii')
        password = client.recv(1024).decode('ascii')
        print("Entry",entry)
        if int(entry) == 2:
            print("reached")
            names.append(name)
            login[name]=password
            clients.append(client)
            client.send("Successfully signed up!".encode('ascii'))
        else:
            if name in names:
                print(1)
                if login[name] == password:
                    index = names.index(name)
                    if(clients[index].fileno()!=-1):
                        client.send("You are logged in elsewhere".encode('ascii'))
                        client.close()
                        continue
                    else:
                        clients[index] = client
                        client.send("Logged In".encode('ascii'))
                else:
                    client.send("Incorrect Password".encode('ascii'))
                    client.close()
                    continue
            else:
                client.send("Username not found, please sign up!".encode('ascii'))
                client.close()
                continue

        print(f"Name of the client is {name}")
        broadcast(f"{name} joined", None)

        thread = threading.Thread(target=handle, args=(client,addr))
        thread.start()

print(f"Server is listening..")
receive()
        
