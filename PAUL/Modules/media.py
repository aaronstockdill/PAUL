"""
media.py
Paul's main media module, to play, pause, etc. At the moment, all interaction
is done with iTunes. I'm working out how to change that.
Author: Aaron Stockdill
"""

import os

import paul

def simple_commands(action):
    ''' Execute simple commands '''
    
    paul.log("MEDIA: " + action)
    
    command = ('osascript -e "tell application \\"iTunes\\" to '
               '{}"'.format(action))
               
    paul.log("COMMAND: " + command)
    
    os.system(command)
    
    return 1
    

def process(sentence):
    ''' Process the sentence '''
    
    sentence.replace_it()
    
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
    
    words = {
        "itunes": ("media", "noun"),
        "music": ("media", "verb"),
        "play": ("media", "verb"), 
        "pause": ("media", "verb"), 
        "stop": ("media", "verb"), 
        "next": ("media", "verb"), 
        "previous": ("media", "verb"), 
        "skip": ("media", "verb"),
        "back": ("media", "verb"),
    }
    
    paul.associate(words)
    paul.vocab.word_actions["media"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()