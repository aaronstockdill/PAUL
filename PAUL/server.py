'''
PAUL Server Program. 
'''
import socket
import threading

import brain

HOST = ''
PORT = 32012

def show_splash():
    import os
    os.system("clear")
    rows, columns = [int(i) for i in os.popen('stty size', 'r').read().split()]
    title = "P.A.U.L Server"
    byline = "Python Actions Using Language, Server v{}".format(
              brain.paul.user_info.info['version'])
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

class Client(threading.Thread):
    
    def __init__(self, socket):
        ''' Handle a new user. '''
        super().__init__()
        self.conn, self.addr = socket
    
    def run(self):
        ''' Run the thread. '''
        print ('Connected: ', self.addr)
        end_line = lambda: self.conn.send(bytes("paul_done" + 1024*" ",
                                                "utf-8"))
        connected = True
        while connected:
            done = False
            data = ""
            while not done:
                inputs = str(self.conn.recv(1024), "utf-8").strip()
                if inputs == "client_done":
                    done = True
                elif inputs == "disconnect":
                    data = -11235
                    done = True
                else:
                    data += inputs
            if data == -11235:
                connected = False
            else:
                brain.paul.user_info.flags["SERVER"] = self.conn
                brain.process(data)
                try:
                    self.conn.send(bytes(" "*1024, "utf-8"))
                    end_line()
                except BrokenPipeError:
                    connected = False
                    break
        self.terminate()
    
    def terminate(self):
        ''' Close the thread '''
        print ('Closing: ', self.addr)
        self.conn.close()
        global connected
        connected.remove(self)
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
show_splash()
print("\nListening on port {}. Press ctrl-C to exit.".format(PORT))
connected = []
while 1:
    try:
        c = Client(s.accept())
        c.start()
        connected.append(c)
    except KeyboardInterrupt:
            for client in connected:
                client.terminate()
            break