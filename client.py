import socket
import select
import sys


HOST = "127.0.0.1"
PORT = 4444
MSG_BUFF=1024
CLIENTS =[sys.stdin]

CLIENT = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
CLIENT.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
CLIENT.connect((HOST,PORT))
CLIENTS.append(CLIENT)


while True:
    
    read,write,err = select.select(CLIENTS,[],[])

    if CLIENT in read:
        MESSAGE = CLIENT.recv(MSG_BUFF)
        MESSAGE=MESSAGE.decode()
        print(MESSAGE)

    if sys.stdin in read:
        CHAT = sys.stdin.readline()
        CHAT = CHAT.encode()
        CLIENT.send(CHAT)

