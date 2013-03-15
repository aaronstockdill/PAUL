from brain import *

print("Enter the command below. Enter 'EXIT' without the quotes to exit.")

exit = False

while not exit:
    command = input("> ")
    if command == "EXIT":
        exit = True
    else:
        print(process(command))