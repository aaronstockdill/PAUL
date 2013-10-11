'''
PAUL Server Program. 
'''
import socket
import brain

HOST = ''
PORT = 32012
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print("\nListening on port {}. Press ctrl-C to exit.".format(PORT))
while 1:
    conn, addr = s.accept()
    print ('Connected: ', addr)
    done = False
    end_line = lambda: conn.send(bytes("paul_done", "utf-8"))
    while not done:
        data = conn.recv(1024)
        if not data:
            done = True
        elif data == "":
            conn.send(bytes("I didn't catch that.", "utf-8"))
            end_line()
        brain.paul.user_info.flags["SERVER"] = conn
        brain.process(str(data, encoding="utf8"))
        try:
            conn.send(bytes(" "*1024, "utf-8"))
            end_line()
        except BrokenPipeError:
            break
    print ('Closing: ', addr)
    conn.close()