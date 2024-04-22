# server
from socket import *
import struct

s = socket(AF_INET, SOCK_STREAM)
host = '127.0.0.1'
port = 40675
s.bind((host, port))
s.listen(5)
c, addr = s.accept()
while True:
    # Receive the length of the message
    length_bytes = c.recv(4)
    if not length_bytes:
        break
    length = struct.unpack('!I', length_bytes)[0]

    # Receive the actual message
    data = b''
    while len(data) < length:
        packet = c.recv(length - len(data))
        if not packet:
            break
        data += packet

    print("client:", data.decode())

    # To leave the while loop write "end"
    if data.decode() == 'Q':
        break

    server_message = input("server: ").encode()

    # Send the length of the server message
    server_message_length = struct.pack('!I', len(server_message))
    c.send(server_message_length)

    # Send the server message
    c.send(server_message)

c.close()