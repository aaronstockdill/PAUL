'''
PAUL server client.
'''

import socket
import os
from sys import argv

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 32012
PROMPT = "?"

def show_splash():
    import os
    os.system("clear")
    rows, columns = [int(i) for i in os.popen('stty size', 'r').read().split()]
    title = "P.A.U.L Client"
    byline = "Python Actions Using Language, Client Mode"
    author = "By Aaron Stockdill"
    w = (columns - len(title))//2
    x = (columns - len(byline))//2
    y = (columns - len(author))//2
    print("\n"
        + " " * w, title + "\n"
        + " " * (w - 1), "=" * (len(title) + 2) + "\n"
        + "\n"
        + " " * x, byline + "\n"
        + " " * y, author + "\n\n")
    print("WARNING: This program is marked for removal from Paul. Cease use.")

def end_line(s):
    s.send(bytes(" "*1024, "utf-8"))
    s.send(bytes("client_done", "utf-8"))
    s.send(bytes(" "*2024, "utf-8"))

def extract_server_info(server_info):
    if server_info == "default":
        host, port = DEFAULT_HOST, DEFAULT_PORT
    else:
        host, port = server_info.split(":")
    return host, int(port)

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
            result = os.popen(data.strip("SCRIPT")).read().strip()
            s.send(bytes(" "*1024, "utf-8"))
            s.send(bytes(result, "utf-8"))
            end_line(s)
        else:
            print(data)



def server_mode(server_info):
    show_splash()
    s = connection(extract_server_info(server_info))
    leave = lambda: s.send(bytes(" " * 1024 + "disconnect", "utf-8"))
    exiting = False
    while not exiting:
        try:
            in_data = input(PROMPT + " ")
            if in_data.lower() == "bye":
                exiting = True
            else:
                s.send(bytes(in_data.strip(), "utf-8"))
                end_line(s)
                show_return(s)
        except KeyboardInterrupt:
            exiting = True
        except EOFError:
            exiting = True
    leave()
    print("Bye!")
    s.close()



def send_single(server_info, string):
    s = connection(extract_server_info(server_info))
    s.send(bytes(string, "utf-8"))
    end_line(s)
    show_return(s)
    s.send(bytes(" " * 1024 + "disconnect", "utf-8"))
    s.close()

if __name__ == "__main__":
    if len(argv) < 2:
        print("USAGE: ./bin/client <host> query\n       <host> is either 'default' or the host.")
    elif len(argv) > 2:
        send_single(argv[1], " ".join(argv[2:]))
    else:
        server_mode(argv[1])