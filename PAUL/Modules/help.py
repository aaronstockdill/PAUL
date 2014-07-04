"""
help.py
The basic help system that Paul comes with.
Author: Aaron Stockdill
"""

import os
import paul
import importlib

def manual():
    ''' Return some helpful info for the user. '''
    s = """
        When you ask for help, I can tell you all sorts of useful info. For
        me to do this, all you need to do is ask! Just say 'help module' and
        I'll tell you about that module. To see a list of modules, just say
        'help'. Easy!
        """
    return s



def get_help(module):
    ''' Given the name of a module as a string, return the help for 
        this module, also as a string. If the module does not have a 
        help function, say so. '''
    def clean(string):
        string = string.replace("\n", " ")
        while "  " in string:
            string = string.replace("  ", " ")
        return string.strip()
    
    if module == "help":
        return clean(manual())
    try:
        m = importlib.import_module("Modules." + module)
        paul.log(m)
        try:
            return clean(m.manual())
        except:
            return "I couldn't find any help for this, I'm afraid. "
    except:
        return "Hmm... I couldn't find that module."


def extract_word(sentence, modules, two_helps=False):
    ''' Extract the module the user wants help with. '''
    for word in modules:
        if sentence.has_word(word):
            if two_helps:
                if word == "help":
                    help_count = 0
                    for w,t in sentence:
                        if w == "help":
                            help_count += 1
                    if help_count > 1:
                        return "help"
                    else:
                        paul.log("NOT ENOUGH HELPS")
                else:
                    return word
            else:
                return word



def process(sentence):
    ''' Process the sentence '''
    r = paul.PAUL_ROOT
    modules = [file[:-3] for file in os.listdir(r + "/Modules/") 
              if file[-3:] == ".py" 
              and file not in [
                  "__init__.py", 
                  "importer.py",
                  "personality.py",
                  "loader.py"]
              ]
    paul.log("MDLS:", modules)
    wrd = extract_word(sentence, modules, two_helps=True)
    if wrd:
        return get_help(wrd)
    helping = "I'm more than happy to help! "
    helping += "I'm able to help with:\n"
    for m in modules:
        helping += "  " + m[0].upper() + m[1:] + "\n"
    paul.interact(helping[:-1])
    r = paul.interact("Which do you want to know about?", response="arb")
    s = paul.Sentence(r)
    if s.has_one_of(["none", "never", "no", "nope", "exit", "stop"]):
        paul.acknowledge()
        return
    wrd = extract_word(s, modules, two_helps=False)
    if wrd:
        return get_help(wrd)
    else:
        return "I wasn't quite sure what you needed help with..."



def main():
    ''' The main function '''
    
    words = {
        "help": ("help", "verb"),
        "stuck": ("help", "verb"),
        "learn": ("help", "verb"),
    }
    
    paul.associate(words)
    paul.register("help", process)

main()