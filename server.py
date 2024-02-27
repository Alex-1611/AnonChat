from socket import *
from threading import *



class Client:
    def __init__(self, (sock, addr)):
        self.sock = sock
        self.addr = addr
    previous = set()

def manage_client(client):



HOST = '192.168.0.185'
PORT = 42069
server = socket (AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

while True:
    client = Client(server.accept())
    th_client=Thread(manage_client(client))
    th_client.start()

