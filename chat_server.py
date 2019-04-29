import socket
import select
from _thread import *
import sys
import message

if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    print("ex: python3 chat_server.py 127.0.0.1 8080\n")
    exit()

IP_address = str(sys.argv[1])
port = int(sys.argv[2])
UDP_port = 8081

# open and bind the UDP handshake socket to listen for new connections
handshake = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
handshake.bind((IP_address, UDP_port))

# AF_INET is the address domain of the socket.
# the second argument is the type of socket, SOCK_STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binds the server to an entered IP address and at the specified port number. Client must be aware of these parameters
server.bind((IP_address, port))
# listens for 100 active connections. This number can be increased as per convenience
server.listen(100)
list_of_clients=[]

print("Chat server started, listening for new connections")

def clientthread(conn, addr):
    # sends a message to the client whose user object is conn
    welcome_msg = "Welcome to the chatroom!"
    conn.send(welcome_msg.encode())

    while True:
        try:
            message = conn.recv(2048) # buffer size 2048 bytes
            if message:
                #User should type in "End Chat" to close the connection
                if message.decode() == "End Chat\n":
                    end_rcvd()
                else:
                    print ("<" + addr[0] + "> " + message.decode())
                    message_to_send = "<" + addr[0] + "> " + message.decode()
                    # prints the message and address of the user who just sent the message on the server terminal
                    broadcast(message_to_send,conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

# if we recieve a HELLO msg from client, begin handshake process over UDP
def hello_rcvd():
    print("Hello recieved")
    # accepts a connection request and stores two parameters, conn which is a socket object for that user,
    # and addr which contains the IP address of the client that just connected
    conn, addr = server.accept()
    # maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    list_of_clients.append(conn)
    # prints the address of the person who just connected
    print (addr[0] + " connected")
    # creates and individual thread for every user that connects
    start_new_thread(clientthread,(conn,addr))
    
def end_rcvd():
    print ("End Request Received") #should acutally close connection, not just say this
    
# listens for messages sent over UDP to handshake port. If we receive a HELLO,
# begin process of authorizing and connecting client via TCP
while True:
    msg, addr = handshake.recvfrom(2048)
    msg_entries = message.unwind_msg(msg.decode())
    if msg_entries[0] == "HELLO":
        hello_rcvd()

handshake.close()
conn.close()
server.close()
