"""
gui.py
The graphical user interface of Paul, one of the main interfaces to PAUL
Author: Aaron Stockdill
"""

from tkinter import *
from tkinter.ttk import *

import brain

class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        
    def think(self, command, label):
        label['text'] = brain.process(command.get())
        command.delete(0, len(command.get()))

        
    def createWidgets(self):
        self.enterText = Entry(self)
        self.enterText.pack()
        self.enterText.bind("<Return>", lambda e: self.think(self.enterText, self.talkLabel))
        self.talkLabel = Label (self, text="Hi!")
        self.goButton = Button (self, text='Go', command=lambda: self.think(self.enterText, self.talkLabel))
        self.endButton = Button (self, text='Bye!', command=lambda: self.master.destroy())
        self.goButton.pack() 
        self.endButton.pack()       
        self.talkLabel.pack()

        
        
paul = Application(Tk())
paul.master.title("PAUL")
paul.mainloop()

