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
    
    command = ('tell application "iTunes" to {}'.format(action))
               
    paul.log("COMMAND: " + command)
    
    paul.run_script(command, language="applescript")
    
    return 1
    

def process(sentence):
    ''' Process the sentence '''
    
    sentence.replace_it()
    
    verbs = sentence.get_part("VB")
    paul.trim_word(verbs, "go")
    paul.log(verbs)
    
    keywords = sentence.keywords()
    paul.log("MUSIC KEYWORDS:", keywords)
    
    commands = {
        'play': lambda x: simple_commands('play ' + key),
        'pause': lambda: simple_commands('pause'),
        'stop': lambda: simple_commands('pause'),
        'next': lambda: simple_commands('next track'),
        'previous': lambda: simple_commands('previous track'),
        'skip': lambda: simple_commands('next track'),
        'forward': lambda: simple_commands('next track'),
        'back': lambda: simple_commands('previous track')
    }
    
    if 'play' not in verbs:
        acknowledge = paul.vocab.vocabulary[verbs[0]]['past_perf']
        try:
            go = commands[verbs[0]]()
        except KeyError:
            return sentence.forward("discover")
    else:
        acknowledge = 'playing'
        if keywords != []:
            key = ('item 1 of (every track of library playlist '
            + '1 whose name is "{}")'.format(keywords[0][0]))
        else:
            key = ""
        try:
            go = commands[verbs[0]](key)
        except KeyError:
            return sentence.forward("discover")
    
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
        "forward": ("media", "verb"),
        "go": ("media", "verb"),
    }
    
    paul.associate(words)
    paul.vocab.word_actions["media"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()