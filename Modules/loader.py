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
             if file != "__init__.py" 
             and file != "__pycache__"
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
    
    known_nouns = {
        "module": lambda sentence: process(sentence), 
        "function": lambda sentence: process(sentence),
    }
    
    known_verbs = {
        "reload": lambda sentence: process(sentence),
        "relaunch": lambda sentence: process(sentence),
        "restart": lambda sentence: process(sentence),
        "reboot": lambda sentence: process(sentence),
    }
    
    user_info.nouns_association.update(known_nouns)
    user_info.verbs_association.update(known_verbs)
    
    if user_info.VERBOSE: print("Successfully imported", __name__)

main()
