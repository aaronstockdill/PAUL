"""
media.py
Paul's main media module, to play, pause, etc. At the moment, all interaction
is done with iTunes. I'm working out how to change that.
Author: Aaron Stockdill
"""

import os

import user_info
import brain2
import vocab

def simple_commands(action):
    ''' Execute simple commands '''
    
    if user_info.VERBOSE: print("MEDIA:", action)
    
    command = ('osascript -e "tell application \\"iTunes\\" to '
               '{}"'.format(action))
               
    if user_info.VERBOSE: print("COMMAND:", command)
    
    os.system(command)
    
    return 1
    

def process(sentence):
    ''' Process the sentence '''
    
    verb = sentence.get_parts("VB")[0]
    
    commands = {
        'play': lambda: simple_commands('play'),
        'pause': lambda: simple_commands('pause'),
        'stop': lambda: simple_commands('pause'),
        'next': lambda: simple_commands('next track'),
        'previous': lambda: simple_commands('previous track'),
        'skip': lambda: simple_commands('next track'),
        'back': lambda: simple_commands('previous track')
    }
    
    if verb != 'play':
        acknowledge = vocab.vocabulary[verb]['past_perf']
    else:
        acknowledge = 'playing'
    go = commands[verb]()
    
    return "OK" if go else "Sorry, that didn't work."

def main():
    ''' The main function '''
    known_nouns = {
        "itunes": lambda sentence: process(sentence),
    }
    
    known_verbs = {
        "play": lambda sentence: process(sentence), 
        "pause": lambda sentence: process(sentence), 
        "stop": lambda sentence: process(sentence), 
        "next": lambda sentence: process(sentence), 
        "previous": lambda sentence: process(sentence), 
        "skip": lambda sentence: process(sentence),
        "back": lambda sentence: process(sentence),
    }
    
    user_info.nouns_association.update(known_nouns)
    user_info.verbs_association.update(known_verbs)
    
    if user_info.VERBOSE: print("Successfully imported", __name__)

main()