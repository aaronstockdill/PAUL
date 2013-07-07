"""
loader.py
A quick program to load all the files in the Modules directory
Author: Aaron Stockdill
"""

import os
import sys
import user_info

def process(sentence):
    ''' Load the files, then restart Paul '''
    
    files = [file[:-3] for file in os.listdir("Modules/") 
             if file[-3:] == ".py" 
             and file != "__init__.py"
             and file != "importer.py"]
    importer = open("Modules/importer.py", 'w')
    for file in files:
        importer.write("import Modules.{0} as {0}\n".format(file))
    importer.write("\nimport vocab\nvocab.add_new()")
    importer.close()
    
    python = sys.executable
    os.execl(python, python, * sys.argv)
        

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
    
    user_info.associate(words)
    user_info.word_actions["loader"] = lambda sentence: process(sentence)
    
    if user_info.VERBOSE: print("Successfully imported", __name__)

main()
