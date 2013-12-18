"""
cli.py
The main interface into PAUL, while the gui is still a bit flakey.
It has two main sections: the standard interface, and the command
line parser.
Author: Aaron Stockdill
"""

import brain
from sys import argv
import os
import time

def show_splash():
    os.system("clear")
    rows, cols = [int(i) for i in os.popen('stty size', 'r').read().split()]
    title =  "P.A.U.L"
    byline = "Python Actions Using Language, v{}".format(
              brain.paul.system.flags['VERSION'])
    author = "By Aaron Stockdill"
    w = (cols - len(title))//2
    x = (cols - len(byline))//2
    y = (cols - len(author))//2
    print("\n"
        + " " * w, title, "\n"
        + " " * (w - 1), "=" * (len(title) + 2) + "\n"
        + "\n"
        + " " * x, byline + "\n"
        + " " * y, author + "\n\n")


def login():
    ''' Attempt to log the user in. '''
    if brain.paul.system.flags["SKIP_LOGIN"] == False:
        name = input("Name: ")
        logged_in = brain.login(name)
        if logged_in:
            print("User found.")
            time.sleep(1)
        else:
            print("User not found.")
            yn = input("Do you wish to log in as a different user? [Y/n] ")
            if yn.lower().startswith("y"):
                login()
            else:
                print("Using default settings.")
                time.sleep(1)
        show_splash()
    else:
        brain.login(brain.paul.system.flags["SKIP_LOGIN"])
    

def main():
    """ The main function, how the system is mostly interacted with. """
    show_splash()
    login()
    print("Type below to interact with Paul.",
          "\nEnter 'bye' without quotes to exit.")

    exit = False
    while not exit:
        try:
            command = input(brain.paul.get_prompt() + " ")
            if command.lower() == "bye":
                exit = True
            else:
                brain.process(command)
        except KeyboardInterrupt:
            exit = True
        except EOFError:
            exit = True
    
    brain.paul.interact("Bye!")


if len(argv) > 1:
    brain.login("default")
    brain.process(" ".join(argv[1:]))
else:
    main()