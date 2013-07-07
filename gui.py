"""
gui.py
The graphical user interface of Paul, one of the main interfaces to PAUL
Author: Aaron Stockdill
"""

from tkinter import *
from tkinter.ttk import *

#from brain_old import *

from brain2 import *
from Modules.importer import *

class Application(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

        
    def think(self, command, label):
        label['text'] = process(command.get())

        
    def createWidgets(self):
        self.enterText = Entry(self)
        self.enterText.grid()
        self.enterText.bind("<Return>", lambda e: self.think(self.enterText, self.talkLabel))
        self.talkLabel = Label (self, text="Hi, I'm Paul")
        self.goButton = Button (self, text='Go', command=lambda: self.think(self.enterText, self.talkLabel))
        self.goButton.grid()        
        self.talkLabel.grid()

        
        
paul = Application()
paul.master.title("PAUL")
paul.mainloop()

