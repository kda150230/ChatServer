import socket
import select
from thread import *
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
list_of_clients=[] # connection sockets
clientIDs=[]

print("Chat server started, listening for new connections")

def clientthread(conn, addr, userID):
    # sends a message to the client whose user object is conn
    welcome_msg = "Welcome to the chatroom!"
    conn.send(welcome_msg.encode())
    flag = -1
    while True:
        try:
            message = conn.recv(2048) # buffer size 2048 bytes
            if message:

                print("Msg = " + message.decode())
                if "CLIENTREQUESTID" in message.decode(): #[0:16 are message, [17] is id (client A's i val)
                    print(message.decode()[15:])
                    print("got here")
                    flag = int(message.decode()[15:])
                    print("CLIENT B FLAG = " + flag)

                # client A requests a chat with client B
                if "Chat" in message.decode():
                    flag = chat_rcvd(message.decode()[5:-1], conn, userID) #send requested client and socket
                #User should type in "End Chat" to close the connection
                elif message.decode() == "Log off\n":
                    end_rcvd()
                else:
                    print ("<" + userID + "> " + message.decode())
                    message_to_send = "<" + userID + "> " + message.decode()
                    # prints the message and address of the user who just sent the message on the server terminal
                    #broadcast(message_to_send[:-1],conn)
                    if flag != -1:
                        list_of_clients[flag].send("<" + userID + "> " + message.encode())
                        conn.send(message.encode())
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
def hello_rcvd(client_id):
    print("Hello recieved")
    # accepts a connection request and stores two parameters, conn which is a socket object for that user,
    # and addr which contains the IP address of the client that just connected
    conn, addr = server.accept()
    # maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    list_of_clients.append(conn)
    clientIDs.append(client_id)
    # prints the address of the person who just connected
    print (client_id + " connected")
    # creates and individual thread for every user that connects
    start_new_thread(clientthread,(conn, addr, client_id))

def end_rcvd():
    print ("End Request Received") #should acutally close connection, not just say this

def chat_rcvd(mess, connection, reqUser): #connection is socket of requesting user, reqUser is requesting user's id
    print ("Chat Request Received")
    print ("Chat Requested with " + mess)

    # determine client ID of the requesting client to send to client B
    for i in range(0, len(clientIDs)):
        if list_of_clients[i] == connection: #client A's own i value
            requester_ival = str(i)

    # loop through clients until we find the client ID we wish to connect to
    for i in range(0, len(clientIDs)):
        if clientIDs[i] == mess: # mess is the requested chat ID of the user.
            print("Client Found")
            try:
                #list_of_clients[i].send(("CHAT_STARTED " + reqUser + "\n").encode())#send message to client
                list_of_clients[i].send(("CLIENTREQUESTID" + requester_ival).encode())
                #connection.send(("CHAT_STARTED " + mess).encode()) #let requested user know chat
                return i
            except:
                print ("Couldn't connect")
                return -1
            # once connected, loop so that we only chat with the other client in our session



# listens for messages sent over UDP to handshake port. If we receive a HELLO,
# begin process of authorizing and connecting client via TCP
while True:
    msg, addr = handshake.recvfrom(2048)
    msg_entries = message.unwind_msg(msg.decode())
    if msg_entries[0] == "HELLO":
        hello_rcvd(msg_entries[1])

handshake.close()
conn.close()
server.close()
