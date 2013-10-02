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
    pp = sentence.get_part("PP", True)
    if pp:
        sentence += pp
    paul.trim_word(keywords, "to")
    paul.log("KEYWORDS:", keywords)
    key = ""
    val = ""
    confirm = "Done!"
    
    settings_file = "PAUL/user_info.py"
    
    if (paul.has_word(keywords, "noisy") 
      or paul.has_word(keywords, "noisiness")
      or paul.has_word(keywords, "talk")
      or paul.has_word(keywords, "talking")):
        key = "NOISY"
    elif (paul.has_word(keywords, "verbose") 
      or paul.has_word(keywords, "verbosity")):
        key = "VERBOSE"
    elif (paul.has_word(keywords, "logging")):
        key  = "LOGGING"
    elif paul.has_word(keywords, "name"):
        key = "name"
    else:
        paul.log("FOUND NEITHER FLAG")
        return "I'm not sure what you wanted we to set."
    
    if paul.has_word(keywords, "off") or paul.has_word(keywords, "false"):
        val = "False"
    elif paul.has_word(keywords, "on") or paul.has_word(keywords, "true"):
        val = "True"
    else:
        if key == "name":
            if sentence.has_word("i"):
                val = paul.join_lists(sentence.get_part("??"), 
                                      sentence.get_part("XO"))
                val = '"{}"'.format(val[0].capitalize())
                confirm = ("Ok, I'll call you " + 
                           "{} from now on.".format(val[1:-1]))
            elif sentence.has_word("you"):
                key = "computer"
                val = paul.join_lists(sentence.get_part("??"), 
                                      sentence.get_part("XO"))
                val = '"{}"'.format(val[0].capitalize())
                confirm = "Ok, I'll be called {}.".format(val[1:-1])
        else:
            paul.log("FOUND NEITHER ON NOR OFF")
            return "I'm not sure if you wanted '{}' on or off.".format(key)
    
    
    sub = "    \"{}\": {},\n".format(key, val)
    paul.log("SETTING:", sub)
    
    lines = open(settings_file).readlines()
    backup = lines[:]
    paul.log("    " + key)
    for i, line in enumerate(lines):
        if line.startswith("    \"" + key + "\""):
            lines[i] = sub
            open(settings_file, "w").write("".join(lines))
            return confirm
    
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
        "logging": ("settings", "noun"),
        "name": ("settings", "noun"),
    }
    
    paul.associate(words)
    paul.vocab.word_actions["settings"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()