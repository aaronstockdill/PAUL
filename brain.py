from os import system
from time import *
from random import choice

increase = ["up", "increase", "raise", "more"]
decrease = ["down", "lower", "decrease", "less"]
mute = ["mute", "silence"]
volume = ["volume", "music", "sound"]
greet = ["hi", "hello", "greetings", "salutations"]
math = ["solve", "answer", "calculate"]
time = ["hour", "time", "morning", "afternoon"]

def process(command):
    words = command.lower().split()
    if any(word in volume for word in words):
        if any(word in increase for word in words):
            result = "I've increased the volume."
            system("osascript -e \"set volume output volume (output volume of (get volume settings) + 6.25)\"")
        elif any(word in decrease for word in words):
            result = "I've lowered the volume."
            system("osascript -e \"set volume output volume (output volume of (get volume settings) - 6.25)\"")
        elif any(word in mute for word in words):
            result = "I've muted the sound."
            system("osascript -e \"set volume output volume 0\"")
        else:
            result = "I don't understand what you want me to do with the volume."
    elif any(word in mute for word in words):
        result = "The computer has been muted."
        system("osascript -e \"set volume output volume 0\"")
    elif any(word in greet for word in words):
        print(choice(greet))
        result = (choice(greet)).title()
    elif any(word in math for word in words):
        result = "The answer is {0}".format(eval(words[1]))
    elif any(word in time for word in words):
        result = "The time is " + asctime()
    else:
        result = "Sorry, I don't understand \"{0}\"".format(command)
    return result