"""
gui.py
The graphical user interface of Paul, one of the main interfaces to PAUL.
Author: Aaron Stockdill
"""

from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import *

import brain
from sys import argv

WIDTH = 500
HEIGHT = 180

def IO(paul):
    def set_text(text, ending=True):
        paul.talkLabel['text'] = text
        paul.output.set(text)
        height = paul.talkLabel.winfo_reqheight()
        paul.master.geometry("500x{}".format(height + 80 if height > 100 else HEIGHT))

    def get_text():
        paul.set_io(2)
        paul.enterText.delete(0, len(paul.enterText.get()))
        paul.wait_variable(paul.response)
        value = paul.response.get()
        paul.set_io(1)
        return value
    return (set_text, get_text)

class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.bg = "#E9E9E9"
        self.pack()
        self.master.configure(bg=self.bg)
        self.master.bind("<Escape>", lambda e: e.widget.quit())
        self.response = StringVar()
        self.output = StringVar()
        if brain.paul.system.flags["SKIP_LOGIN"]:
            self.authenticate(brain.paul.system.flags["SKIP_LOGIN"], True)
        else:
            self.login()
        
    def set_io(self, mode):
        ''' mode 1: think. mode 2: send'''
        if mode == 1:
            f = lambda e: self.think(self.enterText)
            g = lambda: self.think(self.enterText)
        elif mode == 2:
            f = lambda e: self.set_response(self.enterText)
            g = lambda: self.set_response(self.enterText)
        self.goButton.configure(command=g)
        self.enterText.bind("<Return>", f)
        
    def think(self, command):
        com = command.get()
        if com.lower() == "bye":
            self.master.destroy()
        else:
            brain.process(com)
            command.delete(0, len(command.get()))
    
    def set_response(self, command):
        com = command.get()
        self.response.set(com)
        command.delete(0, len(command.get()))
        
    def createWidgets(self):
        self.enterText = Entry(self, width=280)
        self.enterText.bind("<Return>", lambda e: self.think(self.enterText))
        self.talkLabel = Message(self, text="Hi!", 
                                 textvariable=self.output,
                                 width=WIDTH-20, bg=self.bg)
        self.goButton = Button (self, text='Ask...', 
                                command=lambda: self.think(self.enterText))
        self.endButton = Button (self, text='Bye!', 
                                 command=lambda: self.master.destroy())
        self.enterText.pack()
        self.goButton.pack()
        self.endButton.pack()
        self.talkLabel.pack()
    
    
    def purge_login(self):
        self.loginLabel.pack_forget()
        self.userName.pack_forget()
        self.loginButton.pack_forget()
        self.defaultButton.pack_forget()
        self.newUserButton.pack_forget()
    
    
    def new_user(self):
        self.purge_login()
        self.createWidgets()
        logged_in = brain.login('new user')
        # brain.tutorial.run()
    
    
    def authenticate(self, name, skipped=False):
        logged_in = brain.login(name)
        if logged_in:
            if not skipped:
                self.purge_login()
            self.createWidgets()
        else:
            self.loginLabel['text'] = 'Login Failed.'
            self.userName.delete(0, len(name))
            
    
    def login(self):
        self.loginLabel = Label(self, text='User Name:')
        self.loginLabel.pack()
        self.userName = Entry(self)
        self.userName.pack()
        self.userName.bind("<Return>", 
                           lambda e: self.authenticate(self.userName.get()))
        self.loginButton = Button(self, text='Login', 
                           command=lambda: self.authenticate(
                                                self.userName.get()))
        self.loginButton.pack()
        self.defaultButton = Button(self, text='Guest',
                             command=lambda: self.authenticate('default'))
        self.defaultButton.pack()
        self.newUserButton = Button(self, text='New User',
                             command=lambda: self.new_user())
        self.newUserButton.pack()



def setup_gui(paul):
    paul.master.title("P.A.U.L. v{}".format(brain.paul.system.flags['VERSION']))
    w, h = paul.winfo_screenwidth(), paul.winfo_screenheight()
    paul.master.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, 
                                          w/2 - WIDTH/2, h/2 - WIDTH/2))
    paul.master.resizable(0,0)



def main():
    paul = Application(Tk())
    setup_gui(paul)
    res = IO(paul)
    brain.set_IO(res[0], res[1])
    paul.mainloop()



temp_holder = ""
temp_q_holder = ""



def get_text_simple():
    q = temp_holder
    code = ('display dialog "' + q + '" default answer ""\n'
            + 'set res to text returned of result\n'
            + 'return res')
    result = brain.paul.run_script(code, language="applescript", response=True)
    return result



def set_text_simple(text):
    global temp_holder
    temp_holder = text
    brain.paul.send_notification(temp_q_holder, text)



if len(argv) > 1:
    brain.login("default")
    paul = Application(Tk())
    setup_gui(paul)
    brain.set_IO(set_text_simple, get_text_simple)
    temp_q_holder = " ".join(argv[1:])
    brain.process(temp_q_holder)
else:
    main()