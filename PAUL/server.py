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
    while 1:
        data = conn.recv(1024)
        if not data: break
        brain.paul.user_info.flags["SERVER"] = conn
        brain.process(str(data, encoding="utf8"))
        conn.send(bytes("paul_done", "utf-8"))
    print ('Closing: ', addr)
    conn.close()