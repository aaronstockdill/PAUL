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


def login(splash):
    ''' Attempt to log the user in. '''
    if splash:
        print("To log in, enter your username below.")
        print("To create a new user, type 'new user' without quotes.")
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
    

def main(splash=True):
    """ The main function, how the system is mostly interacted with. """
    login(splash)
    if splash: 
        show_splash()
        print("Type below to interact with Paul.",
              "\nEnter 'bye' without quotes to exit.",
              "\n",
              "\nHello, {}".format(brain.paul.system.flags["USER"]["name"]))

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
            print()
        except EOFError:
            exit = True
            print()
    
    brain.paul.interact("Bye!")


if len(argv) > 1:
    brain.login("default")
    items = None
    if argv[1] == "-nw":
        if len(argv) > 2:
            items = argv[2:]
        else:
            main()
    elif argv[1] == '-qnw':
        main(False) 
    else:
        items = argv[1:]
    if items: brain.process(" ".join(items))
else:
    main()