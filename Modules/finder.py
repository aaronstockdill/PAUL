import os
from itertools import *
from operator import *

import user_info
import brain2


def choose(list):
    question = "Which of these do you want?\n"
    options = "\n".join([str(index + 1) + ". " + item.split("/").pop() for 
                         index, item in enumerate(list)])
    choice = brain2.interact(question + options, True)
    if choice is not None:
        return list[choice - 1]
    return None


def join_sequential(items):
    
    words = [item[0] for item in items]
    new_items = []
    for word in words:
        #if word not in ignore:
        word_index = [item[1] for item in items if item[0] == word][0]
        new_items.append((word, word_index))
    
    item_list = []
    for k, g in groupby(enumerate(new_items), lambda i: i[0]-i[1][1]):
        final_items = (list(map(itemgetter(1), g)))
        ind = final_items[0][1]
        final_items = ' '.join([item[0] for item in final_items])
        item_list.append((final_items, ind))
    
    return item_list
    
    

def find(search, params="", look_in=False):
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
    if location:
        message = "Opening {}"
        os.system('open "{}"'.format(location))
        return message.format(location)
    else:
         return "I couldn't find anything."


def reveal(location):
    if location:
        message = "I found {}"
        os.popen('osascript -e "tell application \\"Finder\\" to '
                 'reveal POSIX file \\"{}\\""'.format(location))
        return message.format(location)
    else:
         return "I couldn't find anything."
    
    
def process(sentence):
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
    
    try:
        object = brain2.get_parts(sentence, "NO")[0]
    except:
        object = None
    verb = brain2.get_parts(sentence, "VB")[0]
    
    objects = brain2.get_parts(sentence, "NO", True)
    #catch_wh = brain2.get_parts(sentence, "WH", True)
    preps = brain2.get_parts(sentence, "PP", True)
    names = brain2.get_parts(sentence, "XO", True)
    keywords = brain2.get_parts(sentence, "??", True)
    
    all_together = []
    
    if objects:
        all_together += objects
    #if catch_wh:
        #all_together += catch_wh
    if names:
        all_together += names
    if keywords:
        all_together += keywords
    
    keywords = join_sequential(all_together)
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
    
    else: return commands[verb](find(search, params, where))


def main():
    known_nouns = {
        "file": lambda sentence: process(sentence), 
        "script": lambda sentence: process(sentence), 
        "document": lambda sentence: process(sentence), 
        "image": lambda sentence: process(sentence),
        "folder": lambda sentence: process(sentence),
        "application": lambda sentence: process(sentence),
        "app": lambda sentence: process(sentence),
    }
    
    known_verbs = {
        "open": lambda sentence: process(sentence),
        "launch": lambda sentence: process(sentence),
        "get": lambda sentence: process(sentence),
        "find": lambda sentence: process(sentence),
        "reveal": lambda sentence: process(sentence),
        "locate": lambda sentence: process(sentence),
    }
    
    user_info.nouns_association.update(known_nouns)
    user_info.verbs_association.update(known_verbs)
    
    if user_info.VERBOSE: print("Successfully imported", __name__)

main()