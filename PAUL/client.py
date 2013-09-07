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
        done = False
        while not done:
            data = s.recv(1024)
            data = str(data, encoding="utf8").strip()
            if data == "paul_done":
                done = True
            else:
                print(data)
s.close()