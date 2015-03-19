import socket

credentials = ["root:123456", "root:toor", "admin:123456"]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 1337)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(5)


while True:
    connection, client_address = sock.accept()
    print "[*] New connection from {0}:{1}".format(*client_address)
    try:
        connection.send("Username: ")
        username = connection.recv(32).strip()
        connection.send("Password: ")
        password = connection.recv(32).strip()
        if "{0}:{1}".format(username, password) in credentials:
            connection.send("*"*50 + "\n")
            connection.send("Welcome to really secret control panel.\n")
            connection.send("*"*50 + "\n")
            while True:
                connection.send("$ ")
                data = connection.recv(1024).strip()
                if data == "exit":
                    break
                connection.send("Command not found '{}'\n".format(data))
        else:
            connection.send("Access denied.")
    except socket.error:
        print "An error occured with client ip={0}, port={1}".format(*client_address)

    finally:
        connection.close()