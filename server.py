import socket
import threading
import time

IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, 0)
QUIT = "!quit"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
PORT = server.getsockname()[1]

with open("port.txt",'a') as f:
    f.write(str(PORT))
    f.write('\n')

server.listen()

clients = []
names = []
login = {}

def broadcast(msg, client):
    print(msg)
    messages=msg.split("$-$",1)
    print(messages)
    receiverName = messages[0]
    for c in clients:
        index = clients.index(c)
        if names[index] == receiverName:
            #ADD CODE TO CHECK IF USER IS ONLINE / OFFLINE
            c.send(f'{messages[1]}'.encode('ascii'))
        else:
            continue

def handle(client,addr):
    while True:
        try:
            msg = client.recv(2048).decode('ascii')
            # print(msg[:14])
            if msg[:14]=="query_username":
                # print(5/0)
                # time.sleep(1)
                if(msg[14:] in names):
                    client.send("correct".encode('ascii'))
                    print("c")
                else:
                    client.send("incorrect".encode('ascii'))
                    print("ic")
            elif msg == "logged_out":
                client.close()
                break
            elif msg.split(": ",1)[1] == "/quit":
                print(msg.split(": ",1)[1] == "/quit")
                # index = clients.index(client)
                # clients.remove(client)
                # client.close()
                broadcast(f"{msg.split('$-$',1)[0]}$-${msg.split('$-$',1)[1].split(': ',1)[0]} left",None)
                continue
            else:
                broadcast(msg,client)
                
        except:
            print("0")
            index = clients.index(client)
            # clients.remove(client)
            client.close()
            # name = names(index)
            # names.remove(name)
            # broadcast(f"{names[index]} left",None)
            break

def receive():
    while True:
        try:
            client, addr = server.accept()
            print(f"{addr} connected")

            client.send("entry_type".encode('ascii'))
            entry = client.recv(1024).decode('ascii')
            name = client.recv(1024).decode('ascii')
            password = client.recv(1024).decode('ascii')
            if int(entry) == 2:
                if name in names:
                    client.send("Username by this account already exists, try signing in!".encode('ascii'))
                    client.close()
                    continue
                else:
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
            # broadcast(f"{name} joined", None)

            thread = threading.Thread(target=handle, args=(client,addr))
            thread.start()
        except:
            continue

print(f"Server is listening..")
receive()
        
