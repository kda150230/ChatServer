# ChatServer
CS4391 Final Project

To successfully compile and run this project, it must be done on a UNIX system
First launch the server Script as follows: "python3 chat_server.py 127.0.0.1 8081"
The last two numbers are arbitrary, with the first being the server IP and the latter being the port number
The client script should be compiled in the same way as the server, with the same IP address and port number.
On the client application, the interface is waiting for the user to enter the words "Log on" (case sensitive)
After that, the client will be connected to a general group chat, where anyone connected to the server can message anyone.
To initate a 1-1 connection, the client should type in "Chat" followed by a space and the client's randomly assigned ID #.
Once that is sent, the client will either be connected or rejected.
If connected, messages sent will only be sent to the specific client. To end the chat, simply type "End Chat".
