"""
cli.py
The main interface into PAUL, while the gui is still a bit flakey.
It has two main sections: the standard interface, and the command
line parser.
Author: Aaron Stockdill
"""

import brain
from sys import argv

def main():
    """ The main function, how the system is mostly interacted with """

    print("Enter the command below. Enter 'bye' without the quotes to exit.")

    exit = False

    while not exit:
        try:
            command = input("? ")
            if command.lower() == "bye":
                exit = True
            else:
                brain.process(command)
        except KeyboardInterrupt:
            exit = True
        except EOFError:
            exit = True
    
    brain.paul.interact("\nBye!")



if __name__ == "__main__":
    if len(argv) > 1:
        brain.process(" ".join(argv[1:]))
    else:
        main()