import socket
import threading
import time
import psycopg2
import datetime
import pem
from cryptography.fernet import Fernet

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
    """Sends the personal message to clients

    :param msg: the message content
    :type msg: str
    :param client: connection object with the receiving client
    :type client: socket.socket
    """
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
            print(l)
            if len(l)==0:
                if ":" in messages[1]:
                    sendersName = messages[1].split(": ")[0]    
                else:
                    continue

                x = datetime.datetime.now().strftime("%X")
                curr.execute("INSERT INTO MESSAGES (CONTENT, SENDER, RECEIVER, TIME) VALUES (%s,%s,%s,%s)",(messages[1],sendersName,receiverName,x))
                conn.commit()
                continue
            print(f'--- {l[0][0]}') 
            if l[0][0] == messages[1].split(": ")[0] or l[0][0] == messages[1].split(" ")[0]:
                print("REACHED")
                print(messages[1])
                c.send(f'{messages[1]}'.encode()) 
            else:
                if ":" in messages[1]:
                    sendersName = messages[1].split(": ")[0]    
                else:
                    continue

                x = datetime.datetime.now().strftime("%X")
                curr.execute("INSERT INTO MESSAGES (CONTENT, SENDER, RECEIVER, TIME) VALUES (%s,%s,%s,%s)",(messages[1],sendersName,receiverName,x))
                conn.commit()
                continue
    if not sameServer:
        #add to database
        if ":" in messages[1]:
            sendersName = messages[1].split(": ")[0]
        else:
            return
            # sendersName = messages[1].split(" ")[0]
        x = datetime.datetime.now().strftime("%X")
        curr.execute("INSERT INTO MESSAGES (CONTENT, SENDER, RECEIVER, TIME) VALUES (%s,%s,%s,%s)",(messages[1],sendersName,receiverName,x))
        conn.commit()

def broadcastGroup(msg,client):
    """Module used to send text messages to group-members

    :param msg: message content
    :type msg: str
    :param client: list of connection objects with clients
    :type client: list
    """
    print(msg)
    messages=msg.split("$%$",1)
    groupname = messages[0]
    curr.execute("SELECT USERNAME FROM GPS WHERE GROUPNAME = %s",(groupname,))
    l = curr.fetchall()
    for user in l:
        try:
            index = names.index(user[0])
            c = clients[index]
            curr.execute("SELECT BUDDY FROM CHATROOMS WHERE USERNAME = %s",(user[0]))
            buddy = curr.fetchall()
            print(buddy)
            if c == client:
                continue
            if len(buddy) == 0:
                #add to database
                if ":" in messages[1]:
                    sendersName = messages[1].split(": ")[0]   
                    sendersName = sendersName.split("(")[1][:-1] 
                else:
                    continue
                    # sendersName = messages[1].split(" ")[0]
                # print("SENDER",sendersName)

                x = datetime.datetime.now().strftime("%X")
                curr.execute("INSERT INTO MESSAGES (CONTENT, SENDER, RECEIVER, TIME) VALUES (%s,%s,%s,%s)",(messages[1],sendersName,user[0],x))
                conn.commit()
                continue
            if buddy[0][0] == groupname:
                c.send(f'{messages[1]}'.encode())
            else:
                #add to database
                if ":" in messages[1]:
                    sendersName = messages[1].split(": ")[0] 
                    sendersName = sendersName.split("(")[1][:-1]    
                else:
                    continue
                    # sendersName = messages[1].split(" ")[0]
                # print("SENDER",sendersName)

                x = datetime.datetime.now().strftime("%X")
                curr.execute("INSERT INTO MESSAGES (CONTENT, SENDER, RECEIVER, TIME) VALUES (%s,%s,%s,%s)",(messages[1],sendersName,user[0],x))
                conn.commit()
                continue
        except Exception as e:
            print(e)
            #add to database
            if ":" in messages[1]:
                sendersName = messages[1].split(": ")[0]   
                sendersName = sendersName.split("(")[1][:-1] 
            else:
                sendersName = messages[1].split(" ")[0]
            # print("SENDER",sendersName)

            x = datetime.datetime.now().strftime("%X")
            curr.execute("INSERT INTO MESSAGES (CONTENT, SENDER, RECEIVER, TIME) VALUES (%s,%s,%s,%s)",(messages[1],sendersName,user[0],x))
            conn.commit()
            continue

def broadcastPending(msg,client):
    """Helper function

    :param msg: the message content
    :type msg: str
    :param client: connection object with the client
    :type client: socket.socket
    """
    print(msg=="")
    client.send(msg.encode())
    time.sleep(0.05) 

def broadcastI(imMsg, size, msg,client):
    """Module to send images as personal message to users

    :param imMsg: send the /image message to client, notifying it that an image is to be received
    :type imMsg: str
    :param size: size of imMsg
    :type size: int
    :param msg: the image data encoded into string
    :type msg: str
    :param client: connection object with the client
    :type client: socket.socket
    """
    messages=msg.split("$-$",1)
    receiverName = messages[0]
    sameServer = False
    for c in clients:
        index = clients.index(c)
        if names[index] == receiverName:# and (active_chat[receiverName] == messages[1].split(": ")[0] or active_chat[receiverName] == messages[1].split(" ")[0]):
            sameServer = True
            curr.execute("SELECT BUDDY FROM CHATROOMS WHERE USERNAME = %s",(receiverName,))
            l = curr.fetchall()
            if len(l)==0:
                #add to the database
                if ":" in messages[1]:
                    sendersName = messages[1].split(": ")[0]    
                else:
                    continue
                    # sendersName = messages[1].split(" ")[0]
                # print("SENDER",sendersName)

                x = datetime.datetime.now().strftime("%X")
                curr.execute("INSERT INTO MESSAGES (CONTENT, SENDER, RECEIVER, TIME) VALUES (%s,%s,%s,%s)",(messages[1],sendersName,receiverName,x))
                conn.commit()
                continue
            if l[0][0] == messages[1].split(": ")[0] or l[0][0] == messages[1].split(" ")[0]:
                print("REACHED")
                c.send(imMsg.encode())
                print("116")
                time.sleep(0.05)
                c.send(str(size).encode())
                print("118")
                time.sleep(0.05)
                c.sendall(f'{messages[1]}'.encode())
                time.sleep(0.05)
                print("120")
                print(imMsg)
            else:
                #add to the database
                if ":" in messages[1]:
                    sendersName = messages[1].split(": ")[0]    
                else:
                    continue
                    # sendersName = messages[1].split(" ")[0]
                # print("SENDER",sendersName)

                x = datetime.datetime.now().strftime("%X")
                curr.execute("INSERT INTO MESSAGES (CONTENT, SENDER, RECEIVER, TIME) VALUES (%s,%s,%s,%s)",(messages[1],sendersName,receiverName,x))
                conn.commit()
                continue
    if not sameServer:
        #add to database
        if ":" in messages[1]:
            sendersName = messages[1].split(": ")[0]
        else:
            return
        x = datetime.datetime.now().strftime("%X")
        curr.execute("INSERT INTO MESSAGES (CONTENT, SENDER, RECEIVER, TIME) VALUES (%s,%s,%s,%s)",(messages[1],sendersName,receiverName,x))
        conn.commit()

def handle(client,addr):
    """module which receives messages and signals from the user

    :param client: connection object with the client
    :type client: socket.socket
    :param addr: address of the client
    :type addr: int
    """
    while True:
        try:
            try:
                handleDB(client)
            except:
                continue
            client.settimeout(0.1)
            try:
                msg = client.recv(2048).decode()
            except:
                continue
            client.settimeout(None)

            print(msg)

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
                    curr.execute("SELECT PUBLICKEY FROM CREDS WHERE USERNAME = %s",(receiver,))
                    keyPublic = curr.fetchall()[0][0]
                    client.send(f"{keyPublic}".encode())  
                    print("c")
                else:
                    client.send("incorrect".encode())  
                    print("ic")
            
            elif msg == "logged_out":
                index = clients.index(client)
                curr.execute("DELETE FROM SERVERS WHERE USERNAME = %s",(names[index]))
                clients.remove(client)
                names.remove(names[index])
                client.close()
                conn.commit()
                break
            
            elif msg[:16] == "create_groupname":
                groupinfo = msg[16:].split("$")
                groupname = groupinfo[0]
                grouppass = groupinfo[1]
                curr.execute("SELECT GROUPNAME FROM GPS WHERE GROUPNAME = %s",(groupname,))
                l = curr.fetchall()
                if len(l)!=0:
                    client.send("group_present".encode())
                else:
                    client.send("group_created".encode())
                    pkey = client.recv(1024).decode()
                    index = clients.index(client)
                    curr.execute("INSERT INTO GPS (GROUPNAME,USERNAME,PASSWORD,ISADMIN,PUBLICKEY) VALUES (%s,%s,%s,%s,%s)",(groupname,names[index],grouppass,1,pkey))
                    conn.commit()
            
            elif msg[:15] == "check_groupname":
                groupname = msg[15:]
                curr.execute("SELECT GROUPNAME FROM GPS WHERE GROUPNAME = %s",(groupname,))
                l = curr.fetchall()
                if len(l)!=0:
                    index = clients.index(client)
                    try:
                        curr.execute("SELECT USERNAME FROM GPS WHERE GROUPNAME = %s AND USERNAME = %s",(groupname,names[index]))
                        present = curr.fetchall()
                        if len(present) == 0:
                            client.send("not in group".encode())
                        else:
                            curr.execute("INSERT INTO CHATROOMS (USERNAME, BUDDY) VALUES (%s,%s)",(names[index],groupname))
                            conn.commit()
                            # print("hii")
                            curr.execute("SELECT PUBLICKEY FROM GPS WHERE GROUPNAME = %s AND ISADMIN = 1",(groupname,))
                            l = curr.fetchall()
                            pubkey = l[0][0]
                            client.send(pubkey.encode())
                    except Exception as e:
                        print(e)
                        client.send('group_present')
                else:
                    client.send("no group".encode())
            
            elif msg[:14] == "join_groupname":
                groupinfo = msg[14:].split("$")
                groupname = groupinfo[0]
                grouppass = groupinfo[1]
                curr.execute("SELECT * FROM GPS WHERE GROUPNAME = %s",(groupname,))
                l = curr.fetchall()
                if len(l)!=0:
                    if l[0][2] != grouppass:
                        client.send("Incorrect_pass".encode())
                    else:
                        index = clients.index(client)
                        curr.execute("SELECT * FROM GPS WHERE GROUPNAME = %s AND USERNAME = %s",(groupname,names[index]))
                        l = curr.fetchall()
                        if len(l)!=0:
                            client.send("already".encode())
                        else:
                            client.send("success".encode())
                            curr.execute("SELECT USERNAME FROM GPS WHERE ISADMIN = 1 AND GROUPNAME = %s",(groupname,))
                            l = curr.fetchall()
                            admin = l[0][0]
                            fileName = "pkeys/"+admin+"/"+groupname+"private.pem"
                            privKey = str(pem.parse_file(fileName)[0])
                            client.send(privKey.encode())
                            curr.execute("INSERT INTO GPS (GROUPNAME,USERNAME,PASSWORD,ISADMIN) VALUES (%s,%s,%s,%s)",(groupname,names[index],grouppass,0))
                            conn.commit()
                else:
                    client.send("No group".encode())
            
            elif msg[:12] == "queryPending":
                name = msg[12:]
                print(name)
                curr.execute("SELECT DISTINCT SENDER FROM MESSAGES WHERE RECEIVER = %s",(name,))
                senders = curr.fetchall()
                print(senders)
                if(len(senders) == 0):
                    client.send("no_message".encode())
                    continue
                senderMsg = ""
                for sender in senders:
                    senderMsg += sender[0]+"$"
                print(senderMsg)
                client.send(senderMsg.encode())
                msg = client.recv(1024).decode()
                curr.execute("SELECT CONTENT FROM MESSAGES WHERE SENDER = %s AND RECEIVER = %s ORDER BY TIME",(msg,name))
                msgs = curr.fetchall()
                curr.execute("DELETE FROM MESSAGES WHERE SENDER = %s AND RECEIVER = %s",(msg,name))
                conn.commit()
                for msgTuple in msgs:
                    msg = msgTuple[0]
                    broadcastPending(msg,client)
                time.sleep(0.05)
                client.send("DONE".encode())

            elif msg[:8] == "adminops":
                admin = msg[8:]
                print(admin)
                curr.execute("SELECT GROUPNAME FROM GPS WHERE USERNAME = %s AND ISADMIN = 1",(admin,))
                l = curr.fetchall()
                print(l)
                if(len(l)==0):
                    client.send("noGroups".encode())
                else:
                    groupList = ""
                    for group in l:
                        groupList+=group[0]+"$"
                    groupList = groupList[:-1]
                    print(groupList)
                    client.send(groupList.encode())
                    choice = client.recv(1024).decode()
                    if choice == "!@#$%":
                        continue
                    else:
                        groupchoice = choice.split("!@#")[0]
                        userchoice = choice.split("!@#")[1]
                        curr.execute("SELECT USERNAME FROM GPS WHERE GROUPNAME = %s AND USERNAME = %s",(groupchoice,userchoice))
                        if(len(curr.fetchall())==0):
                            client.send("No such User".endcode())
                            continue
                        else:
                            curr.execute("DELETE FROM GPS WHERE GROUPNAME = %s AND USERNAME = %s",(groupchoice,userchoice))
                            conn.commit()
                            client.send("successfully removed".encode())

            elif msg.split(": ",1)[1] == "/image":
                print("****REC IMAGES*******")
                length = int(client.recv(2048).decode())
                print(length)
                Msg = ""
                while ( len(Msg)<length ):
                    print(len(Msg))
                    Msg=Msg+client.recv(2048).decode()
                print(Msg)
                print(len(Msg))
                print(msg)
                if("$-$" in Msg):
                    broadcastI(msg,length,Msg,client)
                else:
                    pass

            elif "/quit" in msg.split(": ",1)[1]:
                index = clients.index(client)
                curr.execute("DELETE FROM CHATROOMS WHERE USERNAME = %s",(names[index],))
                if "$-$" in msg:
                    broadcast(f"{msg.split('$-$',1)[0]}$-${msg.split('$-$',1)[1].split(': ',1)[0]} left",None)
                    client.send("%$#quitReceive".encode())
                else:
                    broadcastGroup(f"{msg.split('$%$',1)[0]}$%${msg.split('$%$',1)[1].split('(',1)[0]} left",None)
                    client.send("%$#quitReceive".encode())
                continue
            
            else:
                if("$-$" in msg):
                    broadcast(msg,client)
                else:
                    broadcastGroup(msg,client)
                
        except Exception as e:
            print(f"{e}........")
            index = clients.index(client)
            client.close()
            break

def handleDB(client):
    """used to insert, retrieve and delete messages when the user is offline

    :param client: connection object with the client
    :type client: socket.socket
    """
    name = names[clients.index(client)]
    curr.execute("SELECT BUDDY FROM CHATROOMS WHERE USERNAME = %s",(name,))
    buddy = curr.fetchall()
    if len(buddy) == 0:
        pass
    else:
        buddy = buddy[0][0]
        curr.execute("SELECT CONTENT FROM MESSAGES WHERE RECEIVER = %s AND SENDER = %s",(name,buddy))
        msgs = curr.fetchall()
        curr.execute("DELETE FROM MESSAGES WHERE RECEIVER = %s AND SENDER = %s",(name,buddy))
        conn.commit()
        for msg in msgs:
            broadcastPending(msg[0],client)

def receive():
    """handles the login information and password from the user 
    """
    while True:
        try:
            client, addr = server.accept()
            print(f"{addr} connected")
            client.send("entry_type".encode())
            entry = client.recv(1024).decode()
            name = client.recv(1024).decode()
            password = client.recv(1024).decode()
            if int(entry) == 2:
                curr.execute("SELECT USERNAME FROM CREDS WHERE USERNAME = %s",(name,))
                if len(curr.fetchall()) == 1:
                    client.send("Username by this account already exists, try signing in!".encode())
                    client.close()
                    continue
                else:
                    print(name)
                    print(password)
                    names.append(name)
                    clients.append(client)
                    client.send("Successfully signed up!".encode())
                    keyPublic = client.recv(1024).decode()
                    fernetFile = "pkeys/fernet.key"
                    key = open(fernetFile,"rb").read()
                    password = password.encode()
                    x = Fernet(key)
                    password = str(x.encrypt(password))
                    curr.execute("INSERT INTO CREDS (USERNAME, PASSWORD, PUBLICKEY) VALUES (%s,%s,%s)",(str(name), str(password), keyPublic))
                    curr.execute("INSERT INTO SERVERS (USERNAME, PORTS) VALUES (%s,%s)",(str(name),int(PORT)))
                    conn.commit()
            else:
                curr.execute("SELECT USERNAME FROM CREDS WHERE USERNAME=%s",(name,))
                name_ = curr.fetchall()
                # name_ = name_.strip()
                if len(name_) == 1:
                    print(1)
                    curr.execute("SELECT PASSWORD FROM CREDS WHERE USERNAME=%s",(name,))
                    pass_ = curr.fetchall()[0][0]
                    # print(pass_)
                    pass_ = pass_[2:-1].encode()
                    print(pass_)
                    key = open("pkeys/fernet.key","rb").read()
                    x = Fernet(key)
                    pass_ = x.decrypt(pass_).decode()
                    print("password",pass_)
                    if pass_ == password:
                        #if login[name] == password:
                        # index = names.index(name)
                        #Condition to check if you're logged in somewhere else
                        curr.execute("SELECT * FROM SERVERS WHERE USERNAME=%s",(name,))
                        # print("hi")
                        Name = curr.fetchall()
                        if (len(Name)==1):
                        #if(clients[index].fileno()!=-1):
                            client.send("You are logged in elsewhere".encode())
                            client.close()
                            continue
                        else:
                            clients.append(client)
                            names.append(name)
                            curr.execute("INSERT INTO SERVERS(USERNAME, PORTS) VALUES (%s,%s)",(name, PORT))
                            conn.commit()
                            # index = names.index(name)
                            # clients[index] = client
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

            thread = threading.Thread(target=handle, args=(client,addr))
            thread.start()

            # dbthread = threading.Thread(target=handleDB, args=(client,))
            # dbthread.start()

        except Exception as e:
            print(e)
            continue

print(f"Server is listening..")

conn = psycopg2.connect(
   database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
)

curr = conn.cursor()

if __name__=="__main__":
    receive()