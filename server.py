import socket
import select
import sys


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

while True:

    read,write,err = select.select(SOCKETS,[],[])

    for sock in read:
        if sock == SERVER:
            CLIENT,ADDR = SERVER.accept()
            print("Someone connected !!!")
            SOCKETS.append(CLIENT)
        else:
            MESSAGE = sock.recv(MSG_BUFF)
            if not MESSAGE:
                SOCKETS.remove(sock)
                sock.close()
                print("Client disconnected")
                continue
            MESSAGE = MESSAGE.decode()
            print(MESSAGE)
            broadcast(MESSAGE,sock,SOCKETS)