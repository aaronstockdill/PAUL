"""
media.py
Paul's main media module, to play, pause, etc. At the moment, all interaction
is done with iTunes. I'm working out how to change that.
Author: Aaron Stockdill
"""

import os
import paul

def manual():
    ''' Return some helpful info for the user. '''
    s = """
        Who doesn't love a bit of music? I can work with your iTunes Library
        to help you play, pause, skip, go back, and all that stuff. I can even
        play a requested song! And if you want to know what's playing, just ask
        me, and I'll let you know.
        """
    return s



def simple_commands(action):
    ''' Execute simple commands '''
    
    command = ('tell application "iTunes"\ntry\n'
               + '{}\non error errMsg number errorNumber'.format(action)
               + '\nreturn "error"\nend try\nend tell')
    paul.log("MEDIA: " + action)
    paul.log("COMMAND: " + command)
    result = paul.run_script(command, language="applescript", response=True)
    paul.log("RESULT", result)
    if paul.has_word(result.split(), "error"):
        return "I couldn't find your song."
    return True
    

def process(sentence):
    ''' Process the sentence '''
    
    sentence.replace_it()
    
    verbs = sentence.get_part("VB")
    paul.trim_word(verbs, "go")
    paul.log(verbs)
    
    keywords = sentence.keywords(ignore=['song'])
    paul.log("MUSIC KEYWORDS:", keywords)
    
    commands = {
        'play': lambda key: simple_commands('play ' + key),
        'pause': lambda: simple_commands('pause'),
        'stop': lambda: simple_commands('pause'),
        'next': lambda: simple_commands('next track'),
        'previous': lambda: simple_commands('previous track'),
        'skip': lambda: simple_commands('next track'),
        'forward': lambda: simple_commands('next track'),
        'back': lambda: simple_commands('previous track')
    }
    
    if verbs[0] != "play" and verbs[0] in commands.keys():
        try:
            go = commands[verbs[0]]()
        except KeyError:
            return sentence.forward("discover")
    else:
        if keywords != []:
            key = ('item 1 of (every track of library playlist '
            + '1 whose name is "{}")'.format(keywords[0][0]))
        else:
            key = ""
        try:
            go = commands[verbs[0]](key)
        except KeyError:
            if sentence.has_word("what"):
                script = ('tell application "iTunes"\n'
                + '    set myTrack to (name of current track)\n'
                + '    set myArtist to (artist of current track)\n'
                + 'end tell\n\n'
                + 'return "It\'s \'" & myTrack & "\', by " & myArtist & "."')
                res = paul.run_script(script,
                                       language="applescript",
                                       response=True)[:-1]
                if paul.has_one_of(res.split(), ["error", "error:"]):
                    return "I'm not sure."
                return res
                
            return sentence.forward("discover")
    return "Ok." if go is True else go

def main():
    ''' The main function '''
    
    words = {
        "itunes": ("media", "noun"),
        "music": ("media", "noun"),
        "play": ("media", "verb"), 
        "pause": ("media", "verb"), 
        "stop": ("media", "verb"), 
        "next": ("media", "verb"), 
        "previous": ("media", "verb"), 
        "skip": ("media", "verb"),
        "back": ("media", "verb"),
        "forward": ("media", "verb"),
        "go": ("media", "verb"),
        "song": ("media", "noun"),
    }
    
    paul.associate(words)
    paul.register("media", process)

main()