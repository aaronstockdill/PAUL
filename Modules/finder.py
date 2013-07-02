"""
finder.py
This is the filesystem interface for Paul. He can find and open files that
spotlight can find. He ignores some files, though, including library files
and caches, log and property files.
Author: Aaron Stockdill
"""

import os

import user_info
import brain2

NOUNS = [
    'file',
    'folder',
    'powerpoint',
    'keynote',
    'document',
    'word',
    'spreadsheet',
    'excel',
    'picture',
    'image',
    'movie',
    'film',
    'video',
    'audio',
    'music',
    'email',
    'person',
    'contact',
    'event',
    'pdf',
    'preference',
    'bookmark',
    'favourite',
    'font',
    'widget',
    "app", 
    "application", 
    "program", 
    "executable",
    'script',
]

VERBS = [
    "open",
    "launch",
    "get",
    "find",
    "reveal",
    "locate",
]

def choose(list_choices):
    ''' Choose the item from what we found '''
    
    question = "Which of these do you want?\n"
    options = "\n".join([str(index + 1) + ". " + item.split("/").pop() for 
                         index, item in enumerate(list_choices)])
    choice = brain2.interact(question + options, "list")
    if choice is not None:
        if user_info.VERBOSE: print("CHOICE:", choice)
        return list_choices[choice - 1]
    return None
    

def find(search, params="", look_in=False):
    ''' Find the item that was searched for with necessary paramenters '''
    
    if look_in:
        home = look_in
    else:
        home = os.popen('echo $HOME').read().strip('\n')
    
    avoiders = [
        "Library",
        "Cache",
        "~",
        ".log",
        ".properties",
    ]
    
    #home = "/"
    
    command = 'mdfind -onlyin {}/ "{}{}"'.format(home, params, search)
    if user_info.VERBOSE: print("COMMAND:", command)
    
    results = os.popen(command).readlines()
    filtered_results = []
    for line in results:
        line = line.strip("\n")
        append = True
        for avoid in avoiders:
            if avoid in line:
                append = False
        if append:
            filtered_results.append(line)
    if user_info.VERBOSE: print("RESULTS FIRST 5:", filtered_results[:10])
    
    if len(filtered_results) > 0:
        decision = choose(filtered_results[:5])
        if user_info.VERBOSE: print("DECISION:", decision)
        user_info.info["it"] = decision
        if user_info.VERBOSE: print('IT: {}'.format(
                                    user_info.info["it"]))
        return decision
    else:
        return None


def get(location):
    ''' Open the location '''
    
    if location:
        message = "Opening {}"
        os.system('open "{}"'.format(location))
        return message.format(location)
    else:
         return "I couldn't find anything."


def reveal(location):
    ''' Show the location in the Finder '''
    
    if location:
        message = "I found {}"
        os.popen('osascript -e "tell application \\"Finder\\" to '
                 'reveal POSIX file \\"{}\\""'.format(location))
        return message.format(location)
    else:
         return "I couldn't find anything."
    
    
def process(sentence):
    ''' Process the sentence '''
    
    commands = {
        'open': lambda location: get(location),
        'get': lambda location: get(location),
        'launch': lambda location: get(location),
        'show': lambda location: reveal(location),
        'find': lambda location: reveal(location),
        'reveal': lambda location: reveal(location),
        'locate': lambda location: reveal(location),
        'be': lambda location: reveal(location), # Catch in case, use safer reveal than get
    }
    
    types = {
        'file': "",
        'folder': "kind:folder ",
        'powerpoint': "kind:presentation ",
        'keynote': "kind:presentation ",
        'document': "kind:word ",
        'word': "kind:word ",
        'spreadsheet': "kind:spreadsheet ",
        'excel': "kind:spreadsheet ",
        'picture': "kind:image ",
        'image': "kind:image ",
        'movie': "kind:movie ",
        'film': "kind:movie",
        'video': "kind:movie ",
        'audio': "kind:audio ",
        'music': "kind:music ",
        'email': "kind:email ",
        'person': "kind:contact ",
        'contact': "kind:contact ",
        'event': "kind:event ",
        'pdf': "kind:pdf ",
        'preference': "kind:preferences ",
        'bookmark': "kind:bookmark ",
        'favourite': "kind:bookmark ",
        'font': "kind:font ",
        'widget': "kind:widget ",
        "app": "kind:application ", 
        "application": "kind:application ", 
        "program": "kind:application ", 
        "executable": "kind:application ",
    }
    
    sentence.replace_it()
    
    preps = sentence.get_parts("PP")
    if preps:
        if preps[0] == "out":
            return sentence.forward("research")
    
    try:
        object = sentence.get_parts("NO")[0]
    except:
        object = None
    verb = sentence.get_parts("VB")[0]
    
    ignore = list(types.keys()) + list(commands.keys())
    
    keywords = sentence.keywords(ignore)
    if user_info.VERBOSE: print("KEYWORDS:", keywords)
    
    if keywords[0][0] in types.keys():
        get_type = keywords[0][0]
        keywords = keywords[1:]
    else:
        get_type = 'file'
        
    
    apps = ["app", "application", "program", "executable"]
    
    search = keywords[0][0]
    
    if object in apps:
        where = "/Applications"
    else:
        where = False
        params = "{}".format(types[get_type])
    
    if search.startswith("/Users/"): return commands[verb](search)
    elif search.startswith("http"): return commands["open"](search)
    
    else: return commands[verb](find(search, params, where))


def main():
    ''' The main function '''
    
#    known_nouns = {
#        "file": lambda sentence: process(sentence), 
#        "script": lambda sentence: process(sentence), 
#        "document": lambda sentence: process(sentence), 
#        "image": lambda sentence: process(sentence),
#        "folder": lambda sentence: process(sentence),
#        "application": lambda sentence: process(sentence),
#        "app": lambda sentence: process(sentence),
#    }
#    
#    known_verbs = {
#        "open": lambda sentence: process(sentence),
#        "launch": lambda sentence: process(sentence),
#        "get": lambda sentence: process(sentence),
#        "find": lambda sentence: process(sentence),
#        "reveal": lambda sentence: process(sentence),
#        "locate": lambda sentence: process(sentence),
#    }
#    
#    words = {
#        "file": ("finder", "noun"), 
#        "script": ("finder", "noun"), 
#        "document": ("finder", "noun"), 
#        "image": ("finder", "noun"),
#        "folder": ("finder", "noun"),
#        "application": ("finder", "noun"),
#        "app": ("finder", "noun"),
#        "open": ("finder", "verb"),
#        "launch": ("finder", "verb"),
#        "get": ("finder", "verb"),
#        "find": ("finder", "verb"),
#        "reveal": ("finder", "verb"),
#        "locate": ("finder", "verb"),
#        "show": ("finder", "verb"),
#    }
#    
#    user_info.nouns_association.update(known_nouns)
#    user_info.verbs_association.update(known_verbs)

    words = {word: ("finder", "noun") for word in NOUNS}
    words.update({word: ("finder", "verb") for word in VERBS})
    
    #user_info.word_associations.update(words)
    user_info.associate(words)
    user_info.word_actions["finder"] = lambda sentence: process(sentence)
    
    if user_info.VERBOSE: print("Successfully imported", __name__)

main()