import socket
import threading
import time
import psycopg2

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
groups = {}
active_chat = {}

def broadcast(msg, client):
    print(msg)
    messages=msg.split("$-$",1)
    print(messages)
    receiverName = messages[0]
    for c in clients:
        index = clients.index(c)
        if names[index] == receiverName and (active_chat[receiverName] == messages[1].split(": ")[0] or active_chat[receiverName] == messages[1].split(" ")[0]):
            #ADD CODE TO CHECK IF USER IS ONLINE / OFFLINE
            c.send(f'{messages[1]}'.encode())
        else:
            continue

def broadcastGroup(msg,client):
    print(msg)
    messages=msg.split("$%$",1)
    groupname = messages[0]
    for user in groups[groupname]:
        c = user[1]
        if c == client:
            pass
        elif active_chat[user[0]] == groupname:
            c.send(f'{messages[1]}'.encode())




def handle(client,addr):
    while True:
        try:
            msg = client.recv(2048).decode()
            # print(msg[:14])
            if msg[:14]=="query_username":
                # print(5/0)
                # time.sleep(1)
                if(msg[14:] in names):
                    index = clients.index(client)
                    active_chat[names[index]] = msg[14:]
                    client.send("correct".encode())
                    print("c")
                else:
                    client.send("incorrect".encode())
                    print("ic")
            elif msg == "logged_out":

                client.close()
                break
            elif msg[:16] == "create_groupname":
                if msg[16:] in groups.keys():
                    client.send("group_present".encode())
                else:
                    index = clients.index(client)
                    groups[msg[16:]] = [[names[index],client]]
                    client.send("group_created".encode())
            elif msg[:15] == "check_groupname":
                if msg[15:] in groups.keys():
                    index = clients.index(client)
                    active_chat[names[index]] = msg[15:]
                    client.send("group_present".encode())
                else:
                    client.send("no group".encode())
            elif msg[:14] == "join_groupname":
                if msg[14:]in groups.keys():
                    index = clients.index(client)
                    if([names[index],client] in groups[msg[14:]]):
                        client.send("already".encode())
                    else:
                        groups[msg[14:]].append([names[index],client])
                        client.send("success".encode())
                else:
                    client.send("No group".encode())
            elif msg.split(": ",1)[1] == "/quit":
                print(msg.split(": ",1)[1] == "/quit")
                # index = clients.index(client)
                # clients.remove(client)
                # client.close()
                index = clients.index(client)
                active_chat[names[index]] = None
                if "$-$" in msg:
                    broadcast(f"{msg.split('$-$',1)[0]}$-${msg.split('$-$',1)[1].split(': ',1)[0]} left",None)
                else:
                    broadcastGroup(f"{msg.split('$%$',1)[0]}$%${msg.split('$%$',1)[1].split('(',1)[0]} left",None)
                continue
            else:
                if("$-$" in msg):
                    broadcast(msg,client)
                else:
                    broadcastGroup(msg,client)
                
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
            client.send("entry_type".encode())
            entry = client.recv(1024).decode()
            name = client.recv(1024).decode()
            password = client.recv(1024).decode()
            if int(entry) == 2:
                print("IDHER TOH AYEGA HI")
                #if name in creds(USERNAME)
                print(conn)
                curr.execute('''
                            SELECT USERNAME FROM CREDS WHERE USERNAME = '?'
                            ''',(name,))
                name_ = str(curr.fetchone()).strip()
                if name == name_:
                    print("KHO GAYE HUM KHA")
                    client.send("Username by this account already exists, try signing in!".encode())
                    client.close()
                    continue
                else:
                    print("SERVER YHAN AANA CHAHIYE")
                    #change 0 to publickey
                    print(name)
                    print(password)
                    curr.execute("INSERT INTO CREDS (USERNAME, PASSWORD, PUBLICKEY) VALUES (%s,%s,%s)",(str(name), str(password), 'None'))
                    #names.append(name)
                    #login[name]=password
                    print("Chal rha")
                    print(type(PORT))
                    curr.execute("INSERT INTO SERVERS (USERNAME, PORTS, BUDDY) VALUES (%s,%s)",(str(name),int(PORT)))
                    print("COMMIT KRNE JARHA******************")
                    conn.commit()
                    print("COMMIT KRDIYA************************")
                    #clients.append(client)
                    #active_chat[name] = None
                    client.send("Successfully signed up!".encode())
            else:
                curr.execute('''
                            SELECT USERNAME FROM CREDS WHERE USERNAME=?
                            ''',(name,))
                name_ = str(curr.fetchone())
                name_ = name_.strip()
                if name == name_:
                    print(1)
                    curr.execute('''
                            SELECT PASSWORD FROM CREDS WHERE USERNAME=?
                            ''',(name,))
                    pass_ = str(curr.fetchone())
                    pass_ = pass_.strip()
                    if pass_ == password:
                        #if login[name] == password:
                        index = names.index(name)
                        #Condition to check if you're logged in somewhere else
                        curr.execute('''
                            SELECT USERNAME FROM SERVER WHERE USERNAME=?
                        ''',(name,))
                        Name = str(curr.fetchone()).strip()
                        if (Name==name):
                        #if(clients[index].fileno()!=-1):
                            client.send("You are logged in elsewhere".encode())
                            client.close()
                            continue
                        else:
                            curr.execute("INSERT INTO SERVERS(USERNAME, PORTS, PUBLICKEY) VALUES (?,?,?)",(name, PORT, ""))
                            conn.commit()
                            #clients[index] = client
                            #active_chat[name] = None
                            client.send("Logged In".encode())
                    else:
                        client.send("Incorrect Password".encode())
                        client.close()
                        continue
                else:
                    client.send("Username not found, please sign up!".encode())
                    client.close()
                    continue

            print(f"Name of the client is {name}")
            # broadcast(f"{name} joined", None)

            thread = threading.Thread(target=handle, args=(client,addr))
            thread.start()
        except:
            continue

print(f"Server is listening..")

conn = psycopg2.connect(
   database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
)

curr = conn.cursor()

receive()