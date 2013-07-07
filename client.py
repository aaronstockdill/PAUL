'''
PAUL server client.
'''

import socket

HOST = 'localhost'       # The remote host
PORT = 32012
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
exiting = False
while not exiting:
    in_data = input("> ")
    if in_data.lower() == "bye":
        exiting = True
    else:
        s.send(bytes(in_data, "utf-8"))
        data = s.recv(1024)
        print (str(data, encoding="utf8"))
s.close()