"""
settings.py
Change some of Paul's settings straight from Paul himself.
Author: Aaron Stockdill
"""

import os

import paul

def get_key(keywords):
    ''' Decide on the key to use '''
    key = ''
    flag = True
    if paul.has_one_of(keywords, ["noisy", "noisiness", "talk", "talking"]):
        key = "NOISY"
    elif paul.has_one_of(keywords, ["verbose", "verbosity"]):
        key = "VERBOSE"
    elif paul.has_word(keywords, "logging"):
        key  = "LOGGING"
    elif paul.has_one_of(keywords, ["name", "call", "called"]):
        key = "name"
    elif paul.has_word(keywords, "title"):
        key = "title"
    elif paul.has_word(keywords, "prompt"):
        return ("You have to change the prompt in settings"
                + " manually, I'm afraid.", False)
    elif paul.has_one_of(keywords, ["search", "engine", "search engine"]):
        key = "search_engine"
    else:
        paul.log("FOUND NO FLAG")
        return ("I'm not sure what you wanted me to set.", False)
    return (key, flag)
    


def get_val(keywords, key, sentence):
    ''' Determine the value to set. '''
    val = ''
    flag = True
    confirm = "done"
    
    if paul.has_one_of(keywords, ["off", "false", "stop"]):
        val = "False"
    elif paul.has_one_of(keywords, ["on", "true", "start", "begin"]):
        val = "True"
    elif key == "title":
        if paul.has_word(keywords, "sir"):
            val = "sir"
        elif paul.has_word(keywords, "ma'am"):
            val = "ma'am"
        else:
            return ("I don't understand which title " 
                    + "you want to go by, sir or ma'am.", False)
        val = '"{}"'.format(val)
    elif key == "search_engine":
        engines = ["Google", "Bing", "Yahoo", "DuckDuckGo", "Baidu"]
        for engine in engines:
            if paul.has_word(keywords, engine.lower()):
                val = '"{}"'.format(engine)
        if val == '':
            return ("Sorry, I couldn't work out which " 
                    + "search engine you want to use.\n"
                    + "Please choose from Google, Bing, Yahoo, "
                    + "DuckDuckGo and Baidu next time.", False)
    else:
        if key == "name":
            if sentence.has_word("i"):
                val = paul.join_lists(sentence.get_part("??"), 
                                      sentence.get_part("XO"))
                paul.log("VAL[0]", val[0])
                val = '"{}"'.format(val[0].capitalize())
                confirm = ("Ok, I'll call you " + 
                           "{} from now on.".format(val[1:-1]))
            elif sentence.has_word("you"):
                return ("My name is Paul.", False)
        else:
            paul.log("PARAMETER NOT FOUND")
            return ("I'm not sure how you" 
                    + " wanted '{}' set.".format(key), False)
    return (confirm, flag, val)



def make_change(key, val, confirm):
    ''' Write the changes to the user_info file. '''
    settings_file = "PAUL/user_info.py"
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
    
    open(settings_file, "w").write("".join(backup))
    return "Something went wrong changing the setting."



def process(sentence):
    ''' Process the sentence '''
    
    keywords = sentence.keywords(include=["VB", "NS"])
    pp = sentence.get_part("PP", True)
    if pp:
        keywords += pp
    paul.trim_word(keywords, "to")
    
    paul.log("KEYWORDS:", keywords)
    
    temp_key = get_key(keywords)
    if temp_key[1]:
        key = temp_key[0]
    else:
        return temp_key[0]
    
    temp_val = get_val(keywords, key, sentence)
    if temp_val[1]:
        val = temp_val[2]
        confirm = temp_val[0]
    else:
        return temp_val[0]
    
    
    return make_change(key, val, confirm)

def main():
    ''' The main function '''
    
    words = {
        "set": ("settings", "verb"),
        "switch": ("settings", "verb"),
        "turn": ("settings", "verb"),
        "enable": ("settings", "verb"),
        "disable": ("settings", "verb"),
        "change": ("settings", "verb"),
        "begin": ("settings", "verb"),
        "start": ("settings", "verb"),
        "stop": ("settings", "verb"),
        "verbose": ("settings", "noun"),
        "verbosity": ("settings", "noun"),
        "noisy": ("settings", "noun"),
        "noisiness": ("settings", "noun"),
        "talk": ("settings", "noun"),
        "talking": ("settings", "noun"),
        "settings": ("settings", "noun"),
        "logging": ("settings", "noun"),
        "name": ("settings", "noun"),
        "call": ("settings", "verb"),
        "title": ("settings", "noun"),
    }
    
    paul.associate(words)
    paul.vocab.word_actions["settings"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()