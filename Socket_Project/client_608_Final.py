# Import socket module
import socket
import sys

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 4444

# connect to the server on local computer
s.connect(('10.0.0.175', port))

print("You are now connected to your classroom server. Just type yes or no into your input whenever you are asked a question.")
#Clients don't receive any broadcasts from the server, unfortunately.
while True:
  response = input()
  if response.lower() == 'quit':
      s.send("disconnecting from server.".encode())
      sys.exit()
  else:
      s.send(response.encode())

