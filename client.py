import socket
import threading
import sys
import time

IP = socket.gethostbyname(socket.gethostname())
with open("dsPort.txt",'r') as f:
    PORT = int(f.read())
ADDR = (IP, PORT)
# QUIT = "!quit"
client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
client.connect(ADDR)
serverPort = int(client.recv(2048).decode('ascii'))
ADDR = (IP, serverPort)


def receive(client):
    while True:
        try:
            msg = client.recv(2048).decode('ascii')
            if(msg ==  'correct' or msg == 'incorrect'):
                break
            print(msg)
        except:
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
        elif choice==3:
            client.send('logged_out'.encode('ascii'))
            client.close()
            newUser()
            break
        else:
            print(choice)

def DMchatRoom(username,name,client):
    while True:
        client.send(f"query_username{username}".encode('ascii'))
        # time.sleep(0.5)
        msg = client.recv(1024).decode('ascii')
        if msg == "correct" or "incorrect":
            break
    if(msg == "incorrect"):
        print("The entered username does not exist")
        return
    print("Enter \'/quit\' to quit this room")
    print()
    while True:
        msg = f'{username}$-${name}: {input("").strip()}'
        # elif msg.split(": ",1)[1] == QUIT:
        #     client.close()
        #     return
        if msg.split(": ",1)[1]=="/quit":
            client.send(msg.encode('ascii'))
            return
        client.send(msg.encode('ascii'))

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
        msg = client.recv(2048).decode('ascii')
        print(msg)
        print(str(entry))
        if msg == "entry_type":
            client.send(str(entry).encode('ascii'))
            time.sleep(0.05)
            client.send(name.encode('ascii'))
            time.sleep(0.05)
            client.send(password.encode('ascii'))
            msg2 = client.recv(1024).decode('ascii')
            print(msg2)
            if msg2 == "Successfully signed up!" or msg2 == "Logged In":
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

    receive_thread = threading.Thread(target=receive,args=(client,))
    receive_thread.start()

    write_thread = threading.Thread(target=menu,args=(name,client))
    write_thread.start()

newUser()