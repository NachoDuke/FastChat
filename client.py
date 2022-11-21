import socket
import threading
import rsa

IP = socket.gethostbyname(socket.gethostname())
PORT = 7778
ADDR = (IP, PORT)

name = input("Choose a name: ")
id = 0

client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == "Name":
                client.send(name.encode('ascii'))
            elif(msg[:4]=="ID: "):
                id = msg[4:]
                print(id)
            else:
                print(msg)
            
        except:
            print("Error!")
            client.close()
            break

def write():
    while True:
        msg = f'{name}: {input("")}'
        client.send(msg.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()