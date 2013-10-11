'''
PAUL server client.
'''

import socket
import os
from sys import argv

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 32012
PROMPT = "?"

def extract_server_info(server_info):
    if server_info == "default":
        host, port = DEFAULT_HOST, DEFAULT_PORT
    else:
        host, port = server_info.split(":")
    return host, port

def connection(server_info):
    HOST = server_info[0]       # The remote host
    PORT = server_info[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s


def show_return(s):
    done = False
    while not done:
        data = s.recv(1024)
        data = str(data, encoding="utf8").strip()
        if data == "paul_done":
            done = True
        elif data == "":
            pass
        elif data.startswith("SCRIPT"):
            print("SCRIPT:", data.strip("SCRIPT"))
            result = os.popen(data.strip("SCRIPT"))
            s.send(bytes(result.read(), "utf-8"))
        else:
            print(data)



def server_mode(server_info):
    s = connection(extract_server_info(server_info))
    exiting = False
    while not exiting:
        try:
            in_data = input(PROMPT + " ")
            if in_data.lower() == "bye":
                exiting = True
            else:
                s.send(bytes(in_data.strip(), "utf-8"))
                show_return(s)
        except KeyboardInterrupt:
            exiting = True
        except EOFError:
            exiting = True
    print("Bye!")
    s.close()



def send_single(server_info, string):
    s = connection(extract_server_info(server_info))
    s.send(bytes(string, "utf-8"))
    show_return(s)
    s.close()

if __name__ == "__main__":
    if len(argv) < 2:
        print("USAGE: ./bin/client <host> query\n       <host> is either 'default' or the host.")
    elif len(argv) > 2:
        send_single(argv[1], " ".join(argv[2:]))
    else:
        server_mode(argv[1])