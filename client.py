from socket import *
from threading import *
from sys import exit
from rsa import *
from keyboard import *


HELP = ("\n/exit - Stop the program\n"
        "/end - End the chat\n"
        "/search - Search for a new chat\n")

HOST = '192.168.0.185'
PORT = 42069
client = socket(AF_INET, SOCK_STREAM)
in_chat = False
public, private = newkeys(2048)
chat_public = public
def search():
    return client.recv(1).decode('utf-8')
def logic():
    global client, state
    print("Welcome! Type /help for a list of commands.\n")
    client.send(public.save_pkcs1(format="PEM"))
    th1 = Thread(target=sending, args=())
    th1.start()
    th1.join()
def sending():
    global client, in_chat
    th2 = Thread(target=receiving, args=())
    while True:
        msg = input("You: ").strip()
        match(msg):
            case "/help":
                print(HELP)
            case "/exit":
                client.send("0".encode('utf-8'))
                exit(0)
            case "/end":
                client.send("1".encode('utf-8'))
            case "/search":
                if not in_chat:
                    client.send("2".encode('utf-8'))
                    print("Searching...\n"
                          "Press enter to stop searching")
                    th3 = Thread(target=search, args=())
                    th3.start()
                    if is_pressed("enter"):
                        th3.
                else:
                    print('Already in a chat! Type "/end" to end the current chat.')
            case _:
                if msg and msg[0] == "/":
                    print("Invalid command. Try again!")
                elif not in_chat:
                    print('You\'re not in a chat yet! Type "/search" to join one.')
                else:
                    if len(msg.encode('utf-8')) <= 245:
                        client.send(encrypt(msg.encode('utf-8'), chat_public))
                    else:
                        print("Message is too long! Max size is 245 characters.")

def receiving():
    global client, chat_public, in_chat
    chat_public._load_pkcs1_pem(client.recv(512))
    while True:
        msg = client.recv(512)
        if msg == "x".encode('utf-8'):
            print('Chat partner disconnected! Type "/search" to find a new partner.')
            in_chat = False
            break
        else:
            msg = decrypt(msg, private).decode('utf-8')
            print("Anon:" + msg)

while True:
    try:
        client.connect((HOST, PORT))
        print("Connection to the server established.\n")
        client.send(public._save_pkcs1_pem())
        logic()
        break
    except:
        print("Server not available at the moment.\n"
              "/exit - Exit the program\n"
              "/connect - Try connecting to the server\n")
        while True:
            msg = input("You: ")
            match(msg.strip()):
                case "/exit":
                    exit(0)
                case "/connect":
                    break
                case _:
                    print("Invalid command. Try again!")