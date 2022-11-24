import socket
import threading
import sys
import time
import rsa
import base64
import pem
import os

IP = socket.gethostbyname(socket.gethostname())
with open("dsPort.txt",'r') as f:
    PORT = int(f.read())
ADDR = (IP, PORT)
# QUIT = "!quit"
client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
client.connect(ADDR)
serverPort = int(client.recv(2048).decode())
ADDR = (IP, serverPort)

def receive(client,name):
    # print("Inside recieve function")
    while True:
        try:
            # print("$")
            msg = client.recv(2048).decode()
            # print("********************MESSAGE RECIEVED***********************")
            # print(msg)
            if(msg ==  'correct' or msg == 'incorrect'):
                continue
            if(msg == "%$#quitReceive"):
                return
            fileName = "pkeys/"+name+"/"+name+"private.pem"
            with open(fileName,"rb") as f:
                private = rsa.PrivateKey.load_pkcs1(f.read())
                # pr = base64.b64encode(pr)
            if ":" in msg:
                asdf = msg.split(": ",1)[1]
                asdf = asdf[2:-1]
                asdf = asdf.encode().decode('unicode_escape').encode('raw_unicode_escape')
                asdf  = base64.b64decode(rsa.decrypt(asdf,private)).decode()
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
    # print("Inside recieve function")
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
    while True:
        for i in range(5):
            print()
        print("Enter chat room with one user - 1")
        print("Enter chat room with a group - 2")
        print("Log out - 3")
        print("Create a group - 4")
        print("Join a group - 5")
        print("View pending messages - 6")
        choice = int(input("Enter your choice:- ").strip())
        if(choice==1):
            username = input("Enter the username with whom you wish to chat: ").strip()
            client.send(f"query_username{username}".encode())
            # time.sleep(3)
            msg = client.recv(1024).decode()
            # while True:
            #     try:
            #         print(msg," ")
            #         if msg != "":
            #             break
            #     except Exception as e:
            #         print(e)
            #         continue
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
            client.close()
            return
        
        elif choice == 4:
            groupname = input("Enter the group name: ").strip()
            grouppass = input("Enter the goup password: ").strip()
            client.send(f"create_groupname{groupname}${grouppass}".encode())
            msg = client.recv(1024).decode()
            # while True:
            #     print("hi")
            #     # print(f'-- {msg}')
            #     if msg == "group_present" or msg == "group_created":
            #         break
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
            # while True:
            #     if msg == "success" or msg == "No group" or msg == "already":
            #         break
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
                
        else:
            print("Please enter a valid choice!!!")

def DMchatRoom(username,name,client,keyPublic):
    print("Enter \'/quit\' to quit this room")
    print()
    while True:
        usermsg = input().strip()
        if usermsg != "/quit":

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

    try:
        msg = client.recv(2048).decode()
        # print(msg)
        # print(str(entry))
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
    while True:
        while True:
            while True:
                entry = int(input("What do you want to do? \n1. Sign In \n2. Sign Up \n3. Quit\n").strip())
                print("Taken choice as: ",entry)
                if entry != 1 and entry != 2 and entry!=3:
                    print("Invalid input, try again!")
                else:
                    if(entry == 3):
                        # return (0,"")
                        sys.exit()

                    name = input("Enter username: ").strip()
                    print("Confirmed UserName as: ",name)
                    password = input("Enter password: ").strip()
                    print("Confirmed Password as: ",password)
                    break
            client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
            client.connect(ADDR)
            error_code,name = login(client,name,password,entry)
            # if error_code==0:
            #     sys.exit()
            if error_code==1:
                break
            if error_code==2 or error_code==3 or error_code==4 or error_code==5:
                continue

        menu(name,client)

newUser()