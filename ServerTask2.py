import threading
from socket import *

s = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
port = 50000
s.bind((host,port))
s.listen()

clients = []
aliases = []

def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:  # Exclude sender client
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)  # Pass sender client to broadcast
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'), client)  # Pass sender client to broadcast
            aliases.remove(alias)
            break

def receive():
    while True:
        print("server is running and listening...")
        client, addr = s.accept()
        print(f'connection is established with {str(addr)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'the alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the client room'.encode('utf-8'), client)  # Pass sender client to broadcast
        client.send('you are connected!'.encode('utf-8'))
        thread = threading.Thread(target = handle_client, args = (client,))
        thread.start()

receive()