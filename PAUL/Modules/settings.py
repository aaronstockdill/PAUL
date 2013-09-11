"""
settings.py
Change some of Paul's settings straight from Paul himself.
Author: Aaron Stockdill
"""

import os

import paul

def process(sentence):
    ''' Process the sentence '''
    
    keywords = sentence.keywords()
    keywords += sentence.get_part("PP", True)
    paul.trim_word(keywords, "to")
    paul.log("KEYWORDS:", keywords)
    key = ""
    val = ""
    
    settings_file = "PAUL/user_info.py"
    
    if (paul.has_word(keywords, "noisy") 
      or paul.has_word(keywords, "noisiness")
      or paul.has_word(keywords, "talk")
      or paul.has_word(keywords, "talking")):
        key = "NOISY"
    elif (paul.has_word(keywords, "verbose") 
      or paul.has_word(keywords, "verbosity")):
        key = "VERBOSE"
    else:
        paul.log("FOUND NEITHER FLAG")
        return "I'm not sure what you wanted we to set."
    
    if paul.has_word(keywords, "off") or paul.has_word(keywords, "false"):
        val = "False"
    elif paul.has_word(keywords, "on") or paul.has_word(keywords, "true"):
        val = "True"
    else:
        paul.log("FOUND NEITHER ON NOR OFF")
        return "I'm not sure if you wanted '{}' on or off.".format(key)
    
    
    sub = "    \"{}\": {},\n".format(key.upper(), val)
    paul.log("SETTING:", sub)
    
    #paul.log(eval("paul.user_info." + key))
    
    lines = open(settings_file).readlines()
    backup = lines[:]
    paul.log("    " + key.upper())
    for i, line in enumerate(lines):
        if line.startswith("    \"" + key.upper() + "\""):
            lines[i] = sub
            open(settings_file, "w").write("".join(lines))
            return "Done!"
    
    open(settings_file, "w").write("".join(lines))
    
    return "Something went wrong changing the setting."

def main():
    ''' The main function '''
    
    words = {
        "set": ("settings", "verb"),
        "switch": ("settings", "verb"),
        "turn": ("settings", "verb"),
        "verbose": ("settings", "noun"),
        "verbosity": ("settings", "noun"),
        "noisy": ("settings", "noun"),
        "noisiness": ("settings", "noun"),
        "talk": ("settings", "noun"),
        "talking": ("settings", "noun"),
        "settings": ("settings", "noun"),
    }
    
    paul.associate(words)
    paul.vocab.word_actions["settings"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()