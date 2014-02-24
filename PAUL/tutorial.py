'''
tutorial.py
Provide users with a first-time walkthrough.
Author: Aaron Stockdill
'''

def list_abilities():
    ''' Let the user know what Paul is capable of. '''
    pass



def ask_weather():
    ''' Ask the user to get the weather '''
    pass



def say_hello():
    ''' Ask the use to say hello. '''
    greetings = [
        "hi",
        "hello",
        "morning",
        "afternoon",
        "evening",
    ]
    welcome = "Hi there, {}! Lets start with something easy. Say hello!"
    continuing = True
    i = 0
    while continuing:
        recieved = paul.interact(welcome, repsonse="arb")
        if paul.has_one_of(paul.Sentence(recieved), greetings):
            continuing = False
            paul.interact("Fantastic! Moving on...")
        elif i > 3:
            continuing = False
            paul.interact("Never Mind! Moving on...")
        else:
            i += 1
            welcome = "Hmmm, I couldn't understand that,"
            welcome += " lets give it another shot."



def run():
    ''' Run the Tutorial. '''
    say_hello()
    ask_weather()
    list_abilities()