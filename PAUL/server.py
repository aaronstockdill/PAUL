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
    byline = "Python Actions Using Language, Server Mode"
    byline2 = "Based on P.A.U.L. v{}".format(
              brain.paul.user_info.flags['VERSION'])
    author = "By Aaron Stockdill"
    w = (columns - len(title))//2
    x = (columns - len(byline))//2
    y = (columns - len(byline2))//2
    z = (columns - len(author))//2
    print("\n"
        + " " * w, title + "\n"
        + " " * (w - 1), "=" * (len(title) + 2) + "\n"
        + "\n"
        + " " * x, byline + "\n"
        + " " * y, byline2 + "\n"
        + " " * z, author + "\n\n")

class Client(threading.Thread):
    
    def __init__(self, socket):
        ''' Handle a new user. '''
        super().__init__()
        self.conn, self.addr = socket
    
    def send(self, phrase, end=True):
        s = self.conn
        s.send(bytes(" "*1024, "utf-8"))
        s.send(bytes(phrase, 'utf-8'))
        s.send(bytes(" "*1024, "utf-8"))
        if end:
            s.send(bytes("paul_done" + 1024*" ", "utf-8"))
    
    def recv(self):
        s = self.conn
        done = False
        result = ""
        s.send(bytes(" "*1024, "utf-8"))
        while not done:
            come_back = s.recv(1024)
            info = str(come_back, "utf-8").strip()
            brain.paul.log("RECIEVING:", info)
            if info == "client_done":
                brain.paul.log("DONE RECIEVING")
                done = True
            else:
                result += info
        brain.paul.log("RESULT:", result)
        return result
    
    def execute(self, code, response=None):
        s = self.conn
        s.send(bytes(1024*" ", "utf-8"))
        s.send(bytes("SCRIPT{}SCRIPT".format(code), "utf-8"))
        s.send(bytes(1024*" ", "utf-8"))
        if response:
            data = self.recv()
            return data
    
    def run(self):
        ''' Run the thread. '''
        print ('Connected: ', self.addr)
        
        connected = True
        brain.set_IO(self.send, self.recv, self.execute)
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
                try:
                    brain.process(data)
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