"""
gui.py
The graphical user interface of Paul, one of the main interfaces to PAUL.
Author: Aaron Stockdill
"""

from tkinter import *
from tkinter.ttk import *

import brain

REPLY = None

def set_text(text):
    paul.talkLabel['text'] = text

def get_text():
    q = paul.talkLabel['text']
    print(q)
    code = ('display dialog "' + q + '" default answer ""\n'
            + 'set res to text returned of result\n'
            + 'return res')
    result = brain.paul.run_script(code, language="applescript", response=True)
    return result

brain.set_IO(set_text, get_text)

class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        
    def think(self, command):
        com = command.get()
        if com.lower() == "bye":
            self.master.destroy()
        else:
            brain.process(com)
            command.delete(0, len(command.get()))
        
    def createWidgets(self):
        self.enterText = Entry(self)
        self.enterText.pack()
        self.enterText.bind("<Return>", lambda e: self.think(self.enterText))
        self.talkLabel = Label (self, text="Hi!")
        self.goButton = Button (self, text='Go', command=lambda: self.think(self.enterText))
        self.endButton = Button (self, text='Bye!', command=lambda: self.master.destroy())
        self.goButton.pack() 
        self.endButton.pack()       
        self.talkLabel.pack()

        
        
paul = Application(Tk())
paul.master.title("PAUL")
paul.mainloop()

