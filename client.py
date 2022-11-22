import socket
import threading
import sys

IP = socket.gethostbyname(socket.gethostname())
with open("port.txt",'r') as f:
    PORT = int(f.read())
ADDR = (IP, PORT)
QUIT = "!quit"

while True:
    entry = int(input("What do you want to do? \n1. Sign In \n2. Sign Up \n"))
    if entry != 1 and entry != 2:
        print("Invalid input, try again!")
    else:
        name = input("Enter username: ")
        password = input("Enter password: ")
        break

client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    while True:
        # for i in range(2):
            try:
                msg = client.recv(2048).decode('ascii')
                if msg == "entry_type":
                    client.send(str(entry).encode('ascii'))
                    client.send(name.encode('ascii'))
                    client.send(password.encode('ascii'))
                    msg2 = client.recv(1024).decode('ascii')
                    print(msg2)
                    if msg2 == "Succesfully signed up!":
                        pass
                    elif msg2 == "Incorrect Password":
                        client.close()
                        # sys.exit(0)
                        break
                    elif msg2 == "Username not found, please sign up!":
                        client.close()
                        # sys.exit(0)
                        break
                    elif msg2 == "You are logged in elsewhere":
                        client.close()
                        # sys.exit(0)
                        break
                else:
                    print(msg)
                    if(msg ==  'correct' or msg == 'incorrect'):
                        break
                    # if msg == "Succesfully signed up!":
                    #     pass
                    # elif msg == "Incorrect Password":
                    #     client.close()
                    #     sys.exit(0)
                    #     break
                    # elif msg == "Username not found, please sign up!":
                    #     client.close()
                    #     sys.exit(0)
                    #     break
                    # elif msg == "You are logged in elsewhere":
                    #     client.close()
                    #     sys.exit(0)
                    #     break
            except:
                if client.fileno() == -1:
                    break
                else:
                    print("Error!")
                    client.close()
                    break

def menu():
    while True:
        for i in range(5):
            print()
        print("Enter chat room with one user - 1")
        print("Enter chat room with a group - 2")
        print("Log out - 3")
        print("Create a group - 4")
        print("Join a group - 5")
        choice = int(input("Enter your choice:- "))
        if(choice==1):
            name = input("Enter the username with whom you wish to chat: ")
            DMchatRoom(name)
        else:
            print(choice)


def DMchatRoom(name):
    client.send(f"query_username{name}".encode('ascii'))
    msg = client.recv(1024).decode('ascii')
    print(msg)
    return
    if(msg == "incorrect"):
        print("The entered username does not exist")
        return
    print("Enter \'!quit\' to quit this room")
    print()
    while True:
        msg = f'{name}: {input("")}'
        client.send(msg.encode('ascii'))
        if msg.split(": ",1)[1] == QUIT:
            client.close()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=menu)
write_thread.start()