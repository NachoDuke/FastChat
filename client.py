import socket
import threading

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
        try:
            msg = client.recv(2048).decode('ascii')
            if msg == "entry_type":
                client.send(str(entry).encode('ascii'))
                client.send(name.encode('ascii'))
                client.send(password.encode('ascii'))
                # return_msg = client.recv(1024).decode('ascii')
                # print(return_msg)
                # if return_msg == "Successfully signed up!":
                #     pass
                # elif return_msg == "Incorrect Password":
                #     client.close()
                # elif return_msg == "Username not found, please sign up!":
                #     client.close()
            else:
                print(msg)
                if msg == "Succesfully signed up!":
                    pass
                elif msg == "Incorrect Password":
                    client.close()
                    break
                elif msg == "Username not found, please sign up!":
                    client.close()
                    break
        except:
            if client.fileno() == -1:
                break
            else:
                print("Error!")
                client.close()
                break

def write():
    while True:
        msg = f'{name}: {input("")}'
        client.send(msg.encode('ascii'))
        if msg.split(": ",1)[1] == QUIT:
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()