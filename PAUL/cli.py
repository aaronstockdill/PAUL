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

def show_splash():
    import os
    os.system("clear")
    rows, columns = [int(i) for i in os.popen('stty size', 'r').read().split()]
    title =  "P.A.U.L"
    byline = "Python Actions Using Language, v{}".format(
              brain.paul.user_info.info['version'])
    author = "By Aaron Stockdill"
    w = (columns - len(title))//2
    x = (columns - len(byline))//2
    y = (columns - len(author))//2
    print("\n"
        + " " * w, title, "\n"
        + " " * (w - 1), "=" * (len(title) + 2) + "\n"
        + "\n"
        + " " * x, byline + "\n"
        + " " * y, author + "\n\n")

def main():
    """ The main function, how the system is mostly interacted with """

    show_splash()
    print("Type below to interact with Paul.",
          "Enter 'bye' without the quotes to exit.")

    exit = False
    while not exit:
        try:
            command = input(brain.paul.user_info.info["prompt"] + " ")
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
    brain.process(" ".join(argv[1:]))
else:
    main()