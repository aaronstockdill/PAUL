#from brain import *

import brain2
from Modules.importer import *

from sys import argv


if __name__ == "__main__":

    print("Enter the command below. Enter 'bye' without the quotes to exit.")

    exit = False

    while not exit:
        command = input("> ")
        if command.lower() == "bye":
            exit = True
        else:
            #print(process(command))
            brain2.process(command)

def cl_api(sentence):
    brain2.process(sentence)