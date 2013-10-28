"""
loader.py
A quick program to load all the files in the Modules directory
Author: Aaron Stockdill
"""

import os
import sys
import paul

def process(sentence):
    ''' Load the files, then restart Paul '''
    
    files = [file[:-3] for file in os.listdir("PAUL/Modules/") 
             if file[-3:] == ".py" 
             and file != "__init__.py"
             and file != "importer.py"]
    importer = open("PAUL/Modules/importer.py", 'w')
    for file in files:
        importer.write("import Modules.{0} as {0}\n".format(file))
    importer.write("\nimport paul\npaul.update_words()")
    importer.close()
    
    if paul.user_info.flags["SERVER"]:
        return "Restart not supported when in Server Mode."
    else:
        os.execl("/bin/bash", os.getcwd(), "./bin/PAUL")
        

def main():
    ''' The main function '''
    
    words = {
        "module": ("loader", "noun"),
        "function": ("loader", "noun"),
        "load": ("loader", "verb"),
        "reload": ("loader", "verb"),
        "relaunch": ("loader", "verb"),
        "restart": ("loader", "verb"),
        "reboot": ("loader", "verb"),
    }
    
    paul.associate(words)
    paul.vocab.word_actions["loader"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported", __name__)

main()
