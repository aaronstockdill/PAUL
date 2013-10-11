"""
finder.py
This is the filesystem interface for Paul. He can find and open files that
spotlight can find. He ignores some files, though, including library files
and caches, log and property files.
Author: Aaron Stockdill
"""

import os

import paul

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
    choice = paul.interact(question + options, "list")
    if choice is not None:
        paul.log("CHOICE: " + str(choice))
        return list_choices[choice - 1]
    return None
    

def find(params="", look_in=False):
    ''' Find the item that was searched for with necessary paramenters '''
    
    if look_in:
        home = look_in
    else:
        home = paul.run_script('echo $HOME', response=True).strip('\n')
    
    avoiders = [
        "Library",
        "Cache",
        "~",
        ".log",
        ".properties",
    ]
    
    #home = "/"
    
    command = 'mdfind -onlyin {}/ "{}"'.format(home, params)
    
    results = paul.run_script(command, response=True).split("\n")[:-1]
    filtered_results = []
    for line in results:
        line = line.strip("\n")
        append = True
        for avoid in avoiders:
            if avoid in line:
                append = False
        if append:
            filtered_results.append(line)
    paul.log("RESULTS FIRST 5: " + str(filtered_results[:10]))
    
    if len(filtered_results) > 0:
        if len(filtered_results) > 1:
            decision = choose(filtered_results[:5])
        else:
            decision = filtered_results[0]
        paul.log("DECISION: " + str(decision))
        paul.user_info.info["it"] = decision
        paul.log('IT: {}'.format(paul.user_info.info["it"]))
        return decision
    else:
        return None


def get(location):
    ''' Open the location '''
    
    if location:
        message = "Opening {}"
        paul.run_script('open "{}"'.format(location))
        return message.format(location)
    else:
         return "I couldn't find anything."


def reveal(location):
    ''' Show the location in the Finder '''
    
    if location:
        message = "I found {}"
        paul.run_script('tell application "Finder" to '
                        'reveal POSIX file "{}"'.format(location), 
                        language="applescript")
        return message.format(location)
    else:
         return "I couldn't find anything."


def has_position(list, position):
    for item, location in list:
        if position == location:
            return item
    return None


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
        'folder': "folder ",
        'powerpoint': "presentation ",
        'keynote': "presentation ",
        'document': "word ",
        'word': "word ",
        'spreadsheet': "spreadsheet ",
        'excel': "spreadsheet ",
        'picture': "image ",
        'image': "image ",
        'movie': "movie ",
        'film': "movie",
        'video': "movie ",
        'audio': "audio ",
        'music': "music ",
        'email': "email ",
        'event': "event ",
        'pdf': "pdf",
        'preference': "preferences ",
        'bookmark': "bookmark ",
        'favourite': "bookmark ",
        'font': "font ",
        'widget': "widget ",
        "app": "application ", 
        "application": "application ", 
        "program": "application ", 
        "executable": "application ",
    }
    
    replaced = sentence.replace_it()
    
    preps = sentence.get_part("PP", indexes=True)
    
    try:
        object = sentence.get_part("NO")[0]
    except:
        object = None
    verb = sentence.get_part("VB")[0]
    
    if replaced:
        return commands[verb](paul.user_info.info['it'])
    
    ignore = list(types.keys()) + list(commands.keys())
    
    keywords = sentence.keywords(ignore)
    paul.log("KEYWORDS: " + str(keywords))
    
    params_list = []
    
    filters = {
        "from": "(kMDItemFSContentChangeDate == {0} | kMDItemLastUsedDate =={0})",
        "yesterday": "$time.yesterday",
        "today": "$time.today",
        "this week": "$time.this_week",
        "last week": "$time.this_week(-1)",
        "this month": "$time.this_month",
        "this year": "$time.this_year",
        "called": "{}",
        "named": "{}",
        "about": "{}",
    }
    
    for word, position in keywords:
        if preps != None:
            fltr = has_position(preps, position - 1)
        else:
            fltr = None
        if fltr:
            params_list.append(filters[fltr].format(
                                filters.get(word, word)))
        else:
            params_list.append(filters.get(word, word))
            
    
    if keywords == []:
        return "I don't understand. Sorry."
    
    if object in types.keys():
        params_list.append("kind:{}".format(types[object]))
    else:
        pass
        
    
    apps = ["app", "application", "program", "executable"]
    
    if object in apps:
        where = "/Applications"
        params = ""
        paul.log("FINDING APP")
    else:
        where = False
        params = " ".join(params_list)
        paul.log("PARAMETERS: " + str(params))
    
    search = params_list[0]
    paul.log(search)
    
    if search.startswith("http"):
        return commands["open"](search)
    else:
        return commands[verb](find(params, where))


def main():
    ''' The main function '''

    words = {word: ("finder", "noun") for word in NOUNS}
    words.update({word: ("finder", "verb") for word in VERBS})
    
    paul.associate(words)
    paul.vocab.word_actions["finder"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()