# client
from socket import *
import struct

s = socket(AF_INET, SOCK_STREAM)
host = '127.0.0.1'
port = 40675
s.connect((host, port))
print("if you want to terminate the session press 'Q' ")

while True:
    client_message = input("client: ").encode()

    # Send the length of the client message
    client_message_length = struct.pack('!I', len(client_message))
    s.send(client_message_length)

    # Send the client message
    s.send(client_message)

    # To leave while loop write "end"
    if client_message == 'Q':
        break
    # Receive the length of the server message
    length_bytes = s.recv(4)
    if not length_bytes:
        break
    length = struct.unpack('!I', length_bytes)[0]

    # Receive the actual server message
    data = b''
    while len(data) < length:
        packet = s.recv(length - len(data))
        if not packet:
            break
        data += packet

    print("server:", data.decode())

s.close()