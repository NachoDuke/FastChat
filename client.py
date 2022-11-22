import socket
import threading
import sys
import time
import rsa
import base64

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
    while True:
        try:
            a = client.recv(2048)
            msg = a.decode()
            if(msg ==  'correct' or msg == 'incorrect'):
                break
            print(msg)
            # parts = msg.split(": ",1)
            # fileName = "pkeys/"+name + "private.pem"
            # with open(fileName,"rb") as f:
            #     private = rsa.PrivateKey.load_pkcs1(f.read())
            # print("PRIVATE: ",private)
            # print(parts[0],parts[1],sep=": ")
            # a = parts[1].encode()
            # clean = rsa.decrypt(a,private).decode()
            # print(clean)
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
        choice = int(input("Enter your choice:- ").strip())
        if(choice==1):
            username = input("Enter the username with whom you wish to chat: ").strip()
            DMchatRoom(username,name,client)
        elif choice ==2:
            groupname = input("Enter the group name: ").strip()
            while True:
                client.send(f"check_groupname{groupname}".encode())
                msg = client.recv(1024).decode()
                if msg == "group_present" or msg == "no group":
                    break
            if msg == "no group":
                print("The given group does not exist!! Please try again.")
                continue
            else:
                groupchat(groupname,name,client)
        elif choice==3:
            client.send('logged_out'.encode())
            client.close()
            newUser()
            break
        elif choice == 4:
            groupname = input("Enter the group name: ").strip()
            while True:
                client.send(f"create_groupname{groupname}".encode())
                msg = client.recv(1024).decode()
                if msg == "group_present" or msg == "group_created":
                    break
            if msg == "group_present":
                print("A group by this name already exists, please try again")
                continue
            else:
                print("Group successfully created!")
                continue
        elif choice == 5:
            groupname = input("Enter the groupname: ").strip()
            while True:
                client.send(f"join_groupname{groupname}".encode())
                msg = client.recv(1024).decode()
                if msg == "success" or msg == "No group" or msg == "already":
                    break
            if msg == "No group":
                print("There is no such group")
                continue
            elif msg == "already":
                print("You are already a part of this group")
                continue
            else:
                print("You have been added to the group")
                continue
        else:
            print(choice)

def DMchatRoom(username,name,client):
    while True:
        client.send(f"query_username{username}".encode())
        # time.sleep(0.5)
        msg = client.recv(1024).decode()
        if msg == "correct" or "incorrect":
            break
    if(msg == "incorrect"):
        print("The entered username does not exist")
        return
    print("Enter \'/quit\' to quit this room")
    print()
    while True:
        usermsg = input().strip()
        # if usermsg != "/quit":
        #     fileName = "pkeys/"+username + "public.pem"
        #     with open(fileName,"rb") as f:
        #         public = rsa.PublicKey.load_pkcs1(f.read())
        #     print("PUBLIC: ",public)
        #     usermsg = rsa.encrypt(usermsg.encode(),public)
        # # print(usermsg)
        #     usermsg = str(usermsg)
        msg = f'{username}$-${name}: {usermsg}'
        # elif msg.split(": ",1)[1] == QUIT:
        #     client.close()
        #     return
        if msg.split(": ",1)[1]=="/quit":
            client.send(msg.encode())
            return
        # print(msg)
        # fileName = "pkeys/"+username + "private.pem"
        # with open(fileName,"rb") as f:
        #     pr = rsa.PrivateKey.load_pkcs1(f.read())
        # asdf  = rsa.decrypt(msg.encode(),pr).decode()
        client.send(msg.encode())

def groupchat(groupname,name,client):
    print("Enter \'/quit\' to quit this room")
    print()
    while True:
        usermsg = input().strip()
        msg = f'{groupname}$%${name}({groupname}): {usermsg}'
        if msg.split(": ",1)[1]=="/quit":
            client.send(msg.encode())
            return
        client.send(msg.encode())

def login(client,name,password,entry):
    # while True:
    #     entry = int(input("What do you want to do? \n1. Sign In \n2. Sign Up \n3. Quit\n"))
    #     print("Taken choice as: ",entry)
    #     if entry != 1 and entry != 2 and entry!=3:
    #         print("Invalid input, try again!")
    #     else:
    #         if(entry == 3):
    #             client.close()
    #             return (0,"")

    #         name = input("Enter username: ")
    #         print("Confirmed UserName as: ",name)
    #         password = input("Enter password: ")
    #         print("Confirmed Password as: ",password)
    #         break

    try:
        msg = client.recv(2048).decode()
        print(msg)
        print(str(entry))
        if msg == "entry_type":
            client.send(str(entry).encode())
            time.sleep(0.05)
            client.send(name.encode())
            time.sleep(0.05)
            client.send(password.encode())
            msg2 = client.recv(1024).decode()
            print(msg2)
            if msg2 == "Successfully signed up!" or msg2 == "Logged In":
                print("hello")
                publicKey,privateKey = rsa.newkeys(1024)
                
                fileName = "pkeys/"+name + "private.pem"
                with open(fileName,"wb") as f:
                    f.write(privateKey.save_pkcs1("PEM"))
                fileName = "pkeys/"+name + "public.pem"
                with open(fileName,"wb") as f:
                    f.write(publicKey.save_pkcs1("PEM"))

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
            print("wodfb")
    except:
            if client.fileno() == -1:
                return (0,name)
            else:
                print("Error!")
                client.close()
                return (0,name)

def newUser():
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

    receive_thread = threading.Thread(target=receive,args=(client,name))
    receive_thread.start()

    write_thread = threading.Thread(target=menu,args=(name,client))
    write_thread.start()

newUser()