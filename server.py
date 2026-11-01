import socket
import select
import sys
import threading


HOST = "127.0.0.1"
PORT = 4444
MSG_BUFF=1024
SOCKETS =[]

SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.bind((HOST,PORT))
SERVER.listen()
SOCKETS.append(SERVER)

def broadcast(MESSAGE,user,all):
    for sock in all:
        if sock != user and sock != SERVER:
            sock.send(MESSAGE.encode())

def client_handler(CLIENT):
    while True:
        MESSAGE = CLIENT.recv(MSG_BUFF)

        if not MESSAGE:
            SOCKETS.remove(CLIENT)
            CLIENT.close()
            break
        MESSAGE = MESSAGE.decode()
        print(MESSAGE)
        broadcast(MESSAGE, CLIENT, SOCKETS)


while True:

    CLIENT,ADDR = SERVER.accept()
    print("Someone connected !!!")
    SOCKETS.append(CLIENT)

    client_thread = threading.Thread(target=client_handler,args=(CLIENT,))
    client_thread.start()


