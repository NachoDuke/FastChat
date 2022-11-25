import socket
import threading
import sys
import time
import rsa
import base64
import pem
import os
import datetime

IP = socket.gethostbyname(socket.gethostname())
with open("dsPort.txt",'r') as f:
    PORT = int(f.read())
addr = (IP, PORT)

def receive(client,name):
    """The receive module for client. It recieves the messages and images from the server

    :param client: the connection object with server
    :type client: socket.socket
    :param name: name of the user logged in 
    :type name: str
    """
    while True:
        try:
            msg = client.recv(2048).decode()
            if(msg ==  'correct' or msg == 'incorrect'):
                continue
            if(msg == "%$#quitReceive"):
                return
            if ": " in msg:
                if msg.split(": ",1)[1] == "/image":
                    length = int(str(client.recv(2048).decode()))
                    Msg = ""
                    while ( len(Msg)<length ):
                        a = client.recv(2048).decode()
                        time.sleep(0.01)
                        Msg=Msg+a
                    time.sleep(0.05)
                    Msg = Msg.split(": ",2)[2]
                    fileName = "target.jpg"
                    with open(fileName,"wb") as f:
                        S =  Msg[2:].encode('utf-8')
                        a = base64.b64decode(S)
                        f.write(a)
                        f.close()
                    print("You have received a new image from ",msg.split("$-$")[1].split(":")[0], " stored in target.jpg")
                    continue
            fileName = "pkeys/"+name+"/"+name+"private.pem"
            with open(fileName,"rb") as f:
                private = rsa.PrivateKey.load_pkcs1(f.read())
            if ":" in msg:
                asdf = msg.split(": ",1)[1]
                asdf = asdf[2:-1]
                asdf = asdf.encode().decode('unicode_escape').encode('raw_unicode_escape')
                asdf  = base64.b64decode(rsa.decrypt(asdf,private)).decode()
                fileName = "chats/"+name+".txt"
                curr_time = datetime.datetime.now().strftime("%H:%M:%S:%f")
                obj = curr_time.split(":")
                secs = 0
                for i in range(3):
                    secs = secs*60 + int(obj[i])
                secs = secs*1000000 + int(obj[3])
                with open(fileName,"a") as f:
                    s = msg.split(": ",1)[0]+": "+asdf
                    f.write(f"{secs}-{name}$-${s}\n")
                print(msg.split(": ",1)[0]+": "+asdf)
            else:
                print(msg)
        except Exception as e:
            print(e)
            if client.fileno() == -1:
                break
            else:
                print("Error!")
                client.close()
                break

def receiveGroup(client,name,groupname):
    """The receive module of client for groups. Receives text messages and images from group

    :param client: the connection object with server
    :type client: socket.socket
    :param name: name of the user logged in 
    :type name: str
    :param groupname: name of the group
    :type groupname: str
    """
    while True:
        try:
            # print("$")
            msg = client.recv(2048).decode()
            # print("********************MESSAGE RECIEVED***********************")
            # print(msg)
            if(msg == "%$#quitReceive"):
                return
            fileName = "pkeys/"+name+"/"+groupname+"private.pem"
            with open(fileName,"rb") as f:
                private = rsa.PrivateKey.load_pkcs1(f.read())
            if ":" in msg:
                asdf = msg.split(": ",1)[1]
                asdf = asdf[2:-1]
                asdf = asdf.encode().decode('unicode_escape').encode('raw_unicode_escape')
                asdf  = base64.b64decode(rsa.decrypt(asdf,private)).decode()
                fileName = "chats/"+name+".txt"
                curr_time = datetime.datetime.now().strftime("%H:%M:%S:%f")
                obj = curr_time.split(":")
                secs = 0
                for i in range(3):
                    secs = secs*60 + int(obj[i])
                secs = secs*1000000 + int(obj[3])
                with open(fileName,"a") as f:
                    s = msg.split(": ",1)[0]+": "+asdf
                    f.write(f"{secs}-{name}$-${s}\n")
                print(msg.split(": ",1)[0]+": "+asdf)
            else:
                print(msg)
        except Exception as e:
            print(e)
            if client.fileno() == -1:
                break
            else:
                print("Error!")
                client.close()
                break

def menu(name,client):
    """prints the interactive menu for the user. Acts as the front-end

    :param name: name of the user logged in 
    :type name: str
    :param client: the connection object with server
    :type client: socket.socket
    """
    while True:
        for i in range(5):
            print()
        print("Enter chat room with one user - 1")
        print("Enter chat room with a group - 2")
        print("Log out - 3")
        print("Create a group - 4")
        print("Join a group - 5")
        print("View pending messages - 6")
        print("Remove Group Participants(admins only) - 7")
        choice = int(input("Enter your choice:- ").strip())
        if(choice==1):
            username = input("Enter the username with whom you wish to chat: ").strip()
            client.send(f"query_username{username}".encode())
            msg = client.recv(1024).decode()
            if(msg == "incorrect"):
                print("The entered username does not exist")
                continue

            receive_thread = threading.Thread(target=receive,args=(client,name))
            receive_thread.start()

            write_thread = threading.Thread(target=DMchatRoom,args=(username,name,client,msg))
            write_thread.start()

            while True:
                if not receive_thread.is_alive() and not write_thread.is_alive():
                    break

        elif choice ==2:
            groupname = input("Enter the group name: ").strip()
            client.send(f"check_groupname{groupname}".encode())
            msg = client.recv(1024).decode()
            if msg == "no group":
                print("The given group does not exist!! Please try again.")
                continue
            elif msg == "not in group":
                print("You are not a part of this Group, please join first.")
                continue
            else:
                receive_thread = threading.Thread(target=receiveGroup,args=(client,name,groupname))
                receive_thread.start()

                write_thread = threading.Thread(target=groupchat,args=(groupname,name,client,msg))
                write_thread.start()

                while True:
                    if not receive_thread.is_alive() and not write_thread.is_alive():
                        break

        elif choice==3:
            client.send('logged_out'.encode())
            client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
            client.connect((IP,PORT))
            client.send(str(addr[1]).encode())
            client.close()
            return
        
        elif choice == 4:
            groupname = input("Enter the group name: ").strip()
            grouppass = input("Enter the goup password: ").strip()
            client.send(f"create_groupname{groupname}${grouppass}".encode())
            msg = client.recv(1024).decode()
            if msg == "group_present":
                print("A group by this name already exists, please try again")
                continue
            else:
                print("Group successfully created!")
                publicKey,privateKey = rsa.newkeys(1024)
                fileName = "pkeys/"+name+"/"+groupname+"private.pem"
                with open(fileName,"wb") as f:
                    f.write(privateKey.save_pkcs1("PEM"))

                fileName = "pkeys/"+name+"/"+groupname + "public.pem"
                with open(fileName,"wb") as f:
                    f.write(publicKey.save_pkcs1("PEM"))

                keyPublic = str(pem.parse_file(fileName)[0])
                client.send(f"{keyPublic}".encode())
                os.remove(fileName)

                continue
        
        elif choice == 5:
            groupname = input("Enter the groupname: ").strip()
            password = input("Enter the password: ").strip()
            client.send(f"join_groupname{groupname}${password}".encode())
            msg = client.recv(1024).decode()
            if msg == "No group":
                print("There is no such group")
                continue
            elif msg == "already":
                print("You are already a part of this group")
                continue
            elif msg == "Incorrect_pass":
                print("Incorrect password, please try again!")
                continue
            else:
                privateKey = client.recv(1024).decode()
                fileName = "pkeys/"+name+"/"+groupname+"private.pem"
                with open(fileName,'w') as f:
                    f.write(privateKey) 
                print("You have been added to the group")
                continue
        
        elif choice == 6:
            client.send(("queryPending"+name).encode())
            msg = client.recv(1024).decode()
            if(msg == "no_message"):
                print("You have no pending messages from anyone!!!")
                continue
            else:
                try:
                    msg = msg[:-1]
                    senders = msg.split("$")
                    print("You have pending messages from the following groups/users:")
                    senderNo = 1
                    for sender in senders:
                        print(str(senderNo)+ ". "+sender)
                        senderNo=senderNo+1
                    choice = int(input("Choose a number from the above to view:"))
                    if(choice<=len(senders) and choice>0):
                        client.send(senders[choice-1].encode())
                        while True:
                            msg = client.recv(1024).decode()
                            if(msg == "DONE"):
                                break
                            else:
                                if "(" in msg.split(": ")[0]:
                                    fileName = "pkeys/"+name+"/"+senders[choice-1]+"private.pem"
                                else:
                                    fileName = "pkeys/"+name+"/"+name+"private.pem"
                                with open(fileName,"rb") as f:
                                    private = rsa.PrivateKey.load_pkcs1(f.read())
                                    # pr = base64.b64encode(pr)
                                if ":" in msg:
                                    asdf = msg.split(": ",1)[1]
                                    # print(asdf)
                                    asdf = asdf[2:-1]
                                    asdf = asdf.encode().decode('unicode_escape').encode('raw_unicode_escape')
                                    asdf  = base64.b64decode(rsa.decrypt(asdf,private)).decode()
                                    print(msg.split(": ",1)[0]+": "+asdf)
                                else:
                                    print(msg)
                    else:
                        print("Invalid Choice")
                        continue
                except Exception as e:
                    print(e)

        elif choice == 7:
            client.send(("adminops"+name).encode())
            groupList = client.recv(1024).decode()
            print(groupList)
            if(groupList=="noGroups"):
                print("You are not an admin of any groups")
                continue
            else:
                groups = groupList.split("$")
                choice = 1
                for group in groups:
                    print(str(choice)+". "+group)
                choice = int(input("Select one of the above groups"))
                if(choice<=len(groups) and choice >0):
                    group = groups[choice-1]
                    user = input("Enter the username to be removed from the chosen group")
                    group = group +"!@#"+user
                    client.send(group.encode())
                    e = client.recv(1024).decode()
                    if(e=="No such User"):
                        print(e)
                        continue
                    else:
                        print("Successfully removed")
                else:
                    client.send("!@#$%".encode())
                    print("Invalid Input")
                    continue

        else:
            print("Please enter a valid choice!!!")

def DMchatRoom(username,name,client,keyPublic):
    """Module to send direct messages to other users

    :param username: name of the user logged in sending the message
    :type username: str
    :param name: name of the user receiving the message
    :type name: str
    :param client: connection object with the server
    :type client: str
    :param keyPublic: encryption key for the group
    :type keyPublic: str
    """
    print("Enter \'/quit\' to quit this room")
    print("Enter \'/image <imgFile>\' to send an image")
    print()
    while True:
        usermsg = input().strip()
        if usermsg[:6] == "/image":
            location = usermsg[7:]
            if not os.path.exists(location):
                print("No such file exists!")
                continue
            with open(location,"rb") as image:
                a = str(base64.b64encode(image.read()))
                usermsg = usermsg+": "+a
            msg = f'{username}$-${name}: {usermsg}'
            msg_= f'{username}$-${name}: {"/image"}'
            client.send(msg_.encode())
            time.sleep(0.05)
            client.send(str(len(msg.split("$-$")[1])).encode())
            time.sleep(0.05)
            client.sendall(msg.encode())
            time.sleep(10)
            continue
        elif usermsg != "/quit":

            fileName = "pkeys/"+username+"/"+username + "public.pem"
            with open(fileName,"w") as f:
                f.write(keyPublic)
            with open(fileName,"rb") as f:
                public = rsa.PublicKey.load_pkcs1(f.read())

            os.remove(fileName)
            usermsg = rsa.encrypt(base64.b64encode(usermsg.encode()),public)
            usermsg = str(usermsg)
        msg = f'{username}$-${name}: {usermsg}'
        if msg.split(": ",1)[1]=="/quit":
            client.send(msg.encode())
            return
        client.send(msg.encode())

def groupchat(groupname,name,client,keyPublic):
    """Module used to send group chat messages to groups

    :param groupname: name of the group
    :type groupname: str
    :param name: username of the sender
    :type name: str
    :param client: connection object with server
    :type client: socket.socket
    :param keyPublic: encryption key for group
    :type keyPublic: str
    """
    print("Enter \'/quit\' to quit this room")
    print()
    while True:
        usermsg = input().strip()
        if usermsg == "/quit":
            msg = f'{groupname}$%${name}({groupname}): {usermsg}'
            client.send(msg.encode())
            return

        fileName = "pkeys/"+name+"/"+groupname + "public.pem"
        with open(fileName,"w") as f:
            f.write(keyPublic)
        with open(fileName,"rb") as f:
            public = rsa.PublicKey.load_pkcs1(f.read())
        os.remove(fileName)
        usermsg = rsa.encrypt(base64.b64encode(usermsg.encode()),public)
        usermsg = str(usermsg)
        msg = f'{groupname}$%${name}({groupname}): {usermsg}'
        client.send(msg.encode())

def login(client,name,password,entry):
    """send the login information to the server allowing the user to sign-in or sign-up

    :param client: connection object with the server
    :type client: socket.socket
    :param name: username of the user trying to login
    :type name: str
    :param password: password of the account trying to login
    :type password: str
    :param entry: code for sign-in or sign-up
    :type entry: int
    :return: error code or success code
    error_code 1: successful sign-in
    error_code 2: incorrect password
    error_code 3: username not found
    error_code 4: already sign-in somewhere else
    error_code 5: username already exists and cannot be used to make a new account
    :rtype: int
    """
    try:
        msg = client.recv(2048).decode()
        if msg == "entry_type":
            client.send(str(entry).encode())
            time.sleep(0.05)
            client.send(name.encode())
            time.sleep(0.05)
            client.send(password.encode())
            msg2 = client.recv(1024).decode()
            print(msg2)
            if msg2 == "Successfully signed up!" or msg2 == "Logged In":
                if msg2 == "Successfully signed up!":
                    os.mkdir("pkeys//"+name)
                    # print("hello")
                    publicKey,privateKey = rsa.newkeys(1024)
                    
                    fileName = "pkeys/"+name+"/"+name + "private.pem"
                    with open(fileName,"wb") as f:
                        f.write(privateKey.save_pkcs1("PEM"))
                    fileName = "pkeys/"+name+"/"+name + "public.pem"
                    with open(fileName,"wb") as f:
                        f.write(publicKey.save_pkcs1("PEM"))

                    keyPublic = str(pem.parse_file(fileName)[0])
                    client.send(f"{keyPublic}".encode())

                    os.remove(fileName)

                # rsa.PublicKey.
                return (1,name)
            elif msg2 == "Incorrect Password":
                print("Please Try Again")
                return (2,name)
            elif msg2 == "Username not found, please sign up!":
                return (3,name)
            elif msg2 == "You are logged in elsewhere":
                return (4,name)
            elif msg2 == "Username by this account already exists, try signing in!":
                return (5,name)
        else:
            pass
    except Exception as e:
        print(e)
        if client.fileno() == -1:
            return (0,name)
        else:
            print("Error!")
            client.close()
            return (0,name)

def newUser():
    """Prints the login or sign-up menu for the user, when the application is launched
    """
    global addr
    while True:
        while True:
            while True:
                entry = int(input("What do you want to do? \n1. Sign In \n2. Sign Up \n3. Quit\n").strip())
                print("Taken choice as: ",entry)
                if entry != 1 and entry != 2 and entry!=3:
                    print("Invalid input, try again!")
                else:
                    if(entry == 3):
                        sys.exit()

                    name = input("Enter username: ").strip()
                    print("Confirmed UserName as: ",name)
                    password = input("Enter password: ").strip()
                    print("Confirmed Password as: ",password)
                    break

            client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
            client.connect((IP,PORT))
            client.send("route".encode())
            serverPort = int(client.recv(2048).decode())
            addr = (IP, serverPort)
            client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
            client.connect(addr)
            error_code,name = login(client,name,password,entry)
            if error_code==1:
                break
            if error_code==2 or error_code==3 or error_code==4 or error_code==5:
                continue

        menu(name,client)

if __name__=="__main__":    
    newUser()