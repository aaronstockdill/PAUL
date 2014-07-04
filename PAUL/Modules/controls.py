'''
controls.py
This module is designed to give you basic controls over the system. This includes things like volume, screen brightness, sleep, screensaver, etc.
Author: Aaron Stockdill
'''

import os
import paul

VERBS = [
    "lock",
    "sleep",
    "display",
    "show",
    "turn",
    "adjust",
    "set",
    "more",
    "again",
    "mute",
    "louder",
    "quieter",
    "brighter",
    "dimmer",
    "silent",
    "silence",
]

VERBS_UP = [
    "increase",
    "raise",
    "up",
]

VERBS_DOWN = [
    "decrease",
    "lower",
    "down"
]

NOUNS = [
    'volume',
    'screen',
    'system',
    'computer',
    'brightness',
    'screensaver',
    'desktop',
]

screensaver = lambda: paul.run_script(
                        'tell application "ScreenSaverEngine" to activate',
                        language='applescript')

sleep = lambda: paul.run_script('tell application "Finder" to sleep',
                                language='applescript')

desktop = lambda: paul.run_script(
                        'tell application "System Events" to key code 103',
                        language='applescript')

mute = lambda: paul.run_script(
    "set toggle to get volume settings\n"
    + "if output muted of toggle is false then\n"
    + "    set volume with output muted\n"
    + "else\n"
    + "    set volume without output muted\n"
    + "end if",
    language="applescript")

def manual():
    ''' Return some helpful info for the user. '''
    s = """
        If you ever need to tweak anything, I'll give it a go. I can change
        brightness, volume, I can mute, unmute, show the desktop, sleep the
        computer and start your screen saver! Your wish is my command.
        """
    return s



def change_volume(keywords):
    ''' Change the volume up or down, depending on the keywords '''
    
    code = "set volume output volume (output volume of (get volume settings) {} 6.25)"
    if paul.has_one_of(keywords, VERBS_UP+['turn up', 
                                           'adjust up', 
                                           'louder']):
        code = code.format("+")
    elif paul.has_one_of(keywords, VERBS_DOWN+['turn down', 
                                               'adjust down', 
                                               'quieter']):
        code = code.format("-")
    else:
        return "I'm not sure how you wanted me adjust the volume."
    paul.set_it(code)
    paul.run_script(code, language='applescript')
    return "Done!"



def change_brightness(keywords):
    ''' Change the brightness up or down, depending on the keywords '''
    code = 'tell application "System Events" to key code {}'
    up = "113"
    down = "107"
    
    if paul.has_one_of(keywords, VERBS_UP+['turn up', 
                                           'adjust up', 
                                           'brighter']):
        code = code.format(up)
    elif paul.has_one_of(keywords, VERBS_DOWN+['turn down', 
                                               'adjust down', 
                                               'dimmer']):
        code = code.format(down)
    else: 
        return "I can't tell how you wanted the brightness changed."
    paul.set_it(code)
    paul.run_script(code, language='applescript')
    return "Done!"



def repeat():
    ''' Repeat the last action that was done, if it is still stored in "it".
        No argument. Return a string as a response. '''
    it = paul.get_it()
    if it.startswith('tell application "System Events" to key code'):
        paul.run_script(it, language='applescript')
        return "Ok."
    elif it.startswith("set volume output volume (output volume of "):
        paul.run_script(it, language='applescript')
        return "Ok."
    else:
        return "What? I don't understand."



def process(sentence):
    ''' Process the sentence '''
    
    keywords = sentence.keywords(include=['VB', 'NS'])
    paul.log("KEYWORDS:", keywords)
    
    if paul.has_one_of(keywords, ["mute", "silence", "silent, ""unmute"]):
        mute()
        return "Toggling mute."
    elif paul.has_one_of(keywords, ["volume", "louder", "quieter"]):
        return change_volume(keywords)
    elif paul.has_one_of(keywords, ["brightness", "brighter", "dimmer"]):
        return change_brightness(keywords)
    elif paul.has_word(keywords, "screensaver"):
        screensaver()
        return "Done!"
    elif paul.has_word(keywords, "desktop"):
        desktop()
        return "Done!"
    elif paul.has_one_of(keywords, ["lock", "sleep"]):
        sleep()
        return "Done!"
    elif paul.has_one_of(keywords, ["more", "again"]):
        return repeat()
    else:
        return "I couldn't manage that."



def main():
    ''' The main function '''
    words = {}
    
    for word in VERBS + VERBS_UP + VERBS_DOWN:
        words[word] = ("controls", "verb")
    for word in NOUNS:
        words[word] = ("controls", "noun")
    
    paul.associate(words)
    paul.register("controls", process)

main()