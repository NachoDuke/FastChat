import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 7777
ADDR = (IP, PORT)

name = input("Choose a name: ")

client = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == "Name":
                client.send(name.encode('ascii'))
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