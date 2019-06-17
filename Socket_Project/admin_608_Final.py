# Import socket module
import socket
import sys

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 4444

# connect to the server on local computer
s.connect(('10.0.0.175', port))

#admin receives and prints initial message and menu messages
while True:
    msg = s.recv(1024).decode()
    if not msg == "shutdown":
        print(msg)
        response = input()
        s.send(response.encode())
    else:
        print("Administrator disconnected.  Have a nice day!")
        sys.exit()
