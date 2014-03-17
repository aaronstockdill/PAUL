'''
tutorial.py
Provide users with a first-time walkthrough.
Author: Aaron Stockdill
'''

import paul

def list_abilities(fin):
    ''' Let the user know what Paul is capable of. '''
    final_speech = ("Well, I think that gives the basic idea nicely.\n"
                  + "However, my abilities are far greater than "
                  + "telling you the weather. I can also:\n"
                  + "  • Tell the time and date\n"
                  + "  • Control volume and brightness on your computer\n"
                  + "  • Locate and open files\n"
                  + "  • Calculate solutions to equations, including "
                  + "basic Algebra\n"
                  + "  • Play you songs from your iTunes library\n"
                  + "  • Change my own settings\n"
                  + "  • Research a subject using wikipedia\n"
                  + "  • And if all else fails, I can google that for you.\n"
                  + "I think you get the idea. Let's begin.")
    paul.interact(fin + "\n" + final_speech)



def ask_weather():
    ''' Ask the user to get the weather '''
    import Modules.weather as weather
    reply = paul.interact("To get the ball rolling, ask me a question. "
                        + "Let's try\n"
                        + '    "How is the weather?"', response="arb")
    ending = False
    i = 0
    fin = ""
    while not ending:
        sentence = paul.Sentence(reply)
        print(sentence, weather.NOUNS, sentence.has_one_of(weather.NOUNS))
        if i > 3:
            fin = "Doesn't matter. Onward!"
            ending = True
        elif sentence.has_one_of(weather.NOUNS):
            ending = True
            fin = weather.process(sentence)
        else:
            reply = paul.interact("Hmm, that doesn't really sound like a " 
                    + "question about the weather. Give it another shot.",
                    response="arb")
        i += 1
    list_abilities(fin)



def say_hello(name):
    ''' Ask the use to say hello. '''
    greetings = [
        "hi",
        "hello",
        "morning",
        "afternoon",
        "evening",
    ]
    welcome = ("Hi there, {}!".format(name) 
             + " Lets start with something easy. Say hello!")
    continuing = True
    i = 0
    while continuing:
        recieved = paul.interact(welcome, response="arb")
        if paul.has_one_of(paul.Sentence(recieved), greetings):
            continuing = False
            paul.interact("Fantastic! Moving on...")
        elif i > 3:
            continuing = False
            paul.interact("Never mind! Moving on...")
        else:
            i += 1
            welcome = "Hmmm, I couldn't understand that,"
            welcome += " lets give it another shot."
    ask_weather()



def run(name):
    ''' Run the Tutorial. '''
    say_hello(name)