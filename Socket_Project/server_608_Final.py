import matplotlib.pyplot as plt
import socket
import sys
from _thread import *

adminList = []
clientList = []
votes = {}
server_shutdown = False

def adminmenu (conn):
   conn.send("\n\nTo ask a new question, type 'Clear'\nTo show the results, type 'Show'\nTo terminate the server connection, type 'Quit'\nYour selection?".encode())
   menu_input = conn.recv(1024)
   menu_input = (str(menu_input.decode().lower()))
   if menu_input == 'clear':
       clear(votes)
       conn.send("Clearing voting data.\n".encode())
       return False
   if menu_input == 'show':
       show(votes)
       return False
   if menu_input == 'quit':
       for client in clientList:
          client.shutdown(socket.SHUT_RDWR)
          client.close()
       for admin in adminList:
          admin.send("shutdown".encode())
          admin.shutdown(socket.SHUT_RDWR)
          admin.close()
       return True
   else:
       conn.send("Invalid input!".encode())
       return False

def clear(votes):
   votes = votes.clear()
   '''
   The print(votes) function is a debug line to show that this is working
   correctly - in "production code" this should be abstracted so that the
   votes are a secret ballot.
   '''
   print(votes)

def show(dictionary):
   # Pie chart, where the slices will be ordered and plotted counter-clockwise:
   labels = 'No', 'Yes'
   sizes = [list(votes.values()).count('no'), list(votes.values()).count('yes')]
   explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
   fig1, ax1 = plt.subplots()
   ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
      shadow=True, startangle=90)
   ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
   plt.show(block = False)
   plt.pause(2)
   plt.close()

# Admin thread function for first thread created
def adminthread (conn):
   has_exited = False
   conn.send("Welcome, administrator!\nAll connected parties will be able to vote on your in class question: \nPress any key to continue!\n".encode())
   while not has_exited:
       has_exited = adminmenu(conn)
   server_shutdown = True
   conn.close()

# Client thread function called for each new thread after the first
def clientthread(conn, clientNum):
   while server_shutdown == False:
       data = str(conn.recv(32).decode().lower())
       if not data:
          break
       print(clientNum, data)
       if data == 'yes':
           votes[clientNum] = 'yes'
           print(votes)
       elif data == 'no':
           votes[clientNum] = 'no'
           print(votes)
       else:
           pass
   clientList.remove(conn)
   conn.shutdown(socket.SHUT_RDWR)
   conn.close()

# Host information
host = '10.0.0.175'
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket created...")

try:
   s.bind((host,port))
except:
   print('Binding failed')
   sys.exit()

print("Socket bound...")

s.listen(100)

print("Socket is listening...")

while True:
   print("Attempting Connection.")
   conn, addr = s.accept()
   clientNum = str(addr[1])
   print("Connected with " + addr[0] + " : " + str(addr[1]))
   if not adminList:
       adminList.append(conn)
       start_new_thread(adminthread, (conn,))
   else:
       clientList.append(conn)
       start_new_thread(clientthread, (conn, clientNum))
s.close()
sys.exit()
