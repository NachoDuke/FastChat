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
    sameServer = False
    for c in clients:
        index = clients.index(c)
        if names[index] == receiverName:# and (active_chat[receiverName] == messages[1].split(": ")[0] or active_chat[receiverName] == messages[1].split(" ")[0]):
            sameServer = True
            curr.execute("SELECT BUDDY FROM CHATROOMS WHERE USERNAME = %s",(receiverName,))
            l = curr.fetchall()
            print(l[0][0])
            if l[0][0] == messages[1].split(": ")[0] or l[0][0] == messages[1].split(" ")[0]:
                print("REACHED")
                print(messages[1])
                c.send(f'{messages[1]}'.encode())   
            else:
                #add to the database
                pass
    if not sameServer:
        #add to database
        pass

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
                receiver = msg[14:]
                curr.execute("SELECT USERNAME FROM CREDS WHERE USERNAME = %s",(receiver,))
                target = curr.fetchall()
                print(target)
                if(len(target)==1):
                    index = clients.index(client)
                    curr.execute("INSERT INTO CHATROOMS (USERNAME, BUDDY) VALUES (%s,%s)",(names[index],receiver))
                    conn.commit()
                    # active_chat[names[index]] = msg[14:]
                    for i in range(10):
                        try:
                            client.send("correct".encode())
                            time.sleep(0.2)
                        except:
                            continue    
                    print("c")
                else:
                    for i in range(10):
                        try:
                            client.send("incorrect".encode())
                            time.sleep(0.2)
                        except:
                            continue  
                    print("ic")
            elif msg == "logged_out":
                index = clients.index(client)
                curr.execute("DELETE FROM SERVERS WHERE USERNAME = %s",(names[index]))
                client.close()
                conn.commit()
                break
            elif msg[:16] == "create_groupname":
                groupname = msg[16:]
                curr.execute("SELECT GROUPNAME FROM GPS WHERE GROUPNAME = %s",(groupname,))
                l = curr.fetchall()
                if len(l)!=0:
                    client.send("group_present".encode())
                else:
                    index = clients.index(client)
                    curr.execute("INSERT INTO GPS (GROUPNAME,USERNAME) VALUES (%s,%s)",(groupname,names[index]))
                    conn.commit()
                    client.send("group_created".encode())
            elif msg[:15] == "check_groupname":
                groupname = msg[15:]
                curr.execute("SELECT GROUPNAME FROM GPS WHERE GROUPNAME = %s",(groupname,))
                l = curr.fetchall()
                if len(l)!=0:
                    index = clients.index(client)
                    curr.execute("INSERT INTO CHATROOMS (USERNAME, BUDDY) VALUES (%s,%s)",(names[index],groupname))
                    conn.commit()
                    client.send("group_present".encode())
                else:
                    client.send("no group".encode())
            elif msg[:14] == "join_groupname":
                groupname = msg[14:]
                curr.execute("SELECT GROUPNAME FROM GPS WHERE GROUPNAME = %s",(groupname,))
                l = curr.fetchall()
                if len(l)!=0:
                    index = clients.index(client)
                    curr.execute("SELECT * FROM GPS WHERE GROUPNAME = %s AND USERNAME = %s",(groupname,names[index]))
                    l = curr.fetchall()
                    if len(l)!=0:
                        client.send("already".encode())
                    else:
                        # groups[msg[14:]].append([names[index],client])
                        curr.execute("INSERT INTO GPS (GROUPNAME,USERNAME) VALUES (%s,%s)",(groupname,names[index]))
                        conn.commit()
                        client.send("success".encode())
                else:
                    client.send("No group".encode())
            elif msg.split(": ",1)[1] == "/quit":
                print(msg.split(": ",1)[1] == "/quit")
                # index = clients.index(client)
                # clients.remove(client)
                # client.close()
                index = clients.index(client)
                curr.execute("DELETE FROM CHATROOMS WHERE USERNAME = %s",(names[index],))
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
                
        except Exception as e:
            print(e)
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
                # print("IDHER TOH AYEGA HI")
                #if name in creds(USERNAME)
                # print(conn)
                curr.execute("SELECT USERNAME FROM CREDS WHERE USERNAME = %s",(name,))
                if len(curr.fetchall()) == 1:
                    # print("KHO GAYE HUM KHA")
                    client.send("Username by this account already exists, try signing in!".encode())
                    client.close()
                    continue
                else:
                    # print("SERVER YHAN AANA CHAHIYE")
                    #change 0 to publickey
                    print(name)
                    print(password)
                    curr.execute("INSERT INTO CREDS (USERNAME, PASSWORD, PUBLICKEY) VALUES (%s,%s,%s)",(str(name), str(password), 'None'))
                    names.append(name)
                    #login[name]=password
                    # print("Chal rha")
                    # print(type(PORT))
                    curr.execute("INSERT INTO SERVERS (USERNAME, PORTS) VALUES (%s,%s)",(str(name),int(PORT)))
                    # print("COMMIT KRNE JARHA******************")
                    conn.commit()
                    # print("COMMIT KRDIYA************************")
                    clients.append(client)
                    #active_chat[name] = None
                    client.send("Successfully signed up!".encode())
            else:
                curr.execute("SELECT USERNAME FROM CREDS WHERE USERNAME=%s",(name,))
                name_ = curr.fetchall()
                # name_ = name_.strip()
                if len(name_) == 1:
                    print(1)
                    curr.execute("SELECT PASSWORD FROM CREDS WHERE USERNAME=%s",(name,))
                    pass_ = curr.fetchone()[0]
                    pass_ = pass_.strip()
                    if pass_ == password:
                        #if login[name] == password:
                        # index = names.index(name)
                        #Condition to check if you're logged in somewhere else
                        curr.execute("SELECT * FROM SERVERS WHERE USERNAME=%s",(name,))
                        Name = curr.fetchall()
                        if (len(Name)==1):
                        #if(clients[index].fileno()!=-1):
                            client.send("You are logged in elsewhere".encode())
                            client.close()
                            continue
                        else:
                            curr.execute("INSERT INTO SERVERS(USERNAME, PORTS) VALUES (%s,%s,%s)",(name, PORT))
                            conn.commit()
                            index = names.index(name)
                            clients[index] = client
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
        except Exception as e:
            print(e)
            continue

print(f"Server is listening..")

conn = psycopg2.connect(
   database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
)

curr = conn.cursor()

receive()