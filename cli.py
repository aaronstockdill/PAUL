"""
cli.py
The main interface into PAUL, while the gui is still a bit flakey.
It has two main sections: the standard interface, and the command
line parser.
Author: Aaron Stockdill
"""

#from brain_old import *
#import brain2

import brain
from sys import argv

def main():
    """ The main function, how the system is mostly interacted with """

    print("Enter the command below. Enter 'bye' without the quotes to exit.")

    exit = False

    while not exit:
        command = input("? ")
        if command.lower() == "bye":
            exit = True
        else:
            #print(process(command))
            #brain2.process(command)
            brain.process(command)
    #brain2.interact("Bye!")
    brain.interact("Bye!")

def cl_api(sentence):
    """ The 'paul' interface """
    
    brain2.process(sentence)

if __name__ == "__main__":
    main()