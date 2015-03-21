import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 1337)

sock.connect(server_address)

data = ""
last_data = ""

while True:
    last_data = sock.recv(1024)
    if last_data:
        data += last_data
    else:
        break
