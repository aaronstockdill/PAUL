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

def manual():
    ''' Return some helpful info for the user. '''
    s = """
        Finder is all about your stuff. If you have a file you want to work
        with, I will do my best to track it down. You can then open it, or get
        me to show you where it is in the Finder. If there are two files with
        the same name, I'll ask you which one you want me to open.
        """
    return s



def choose(list_choices):
    ''' Choose the item from what we found '''
    
    question = "Which of these do you want? \n"
    options = "\n".join([str(index + 1) + ". " +
                         "/".join(item.split("/")[3:]) for 
                         index, item in enumerate(list_choices)])
    choice = paul.interact(question + options, "list")
    if choice is not None and choice <= 5 and choice > 0:
        paul.log("CHOICE: " + str(choice))
        return list_choices[choice - 1]
    return None


def has_one_of_substrings(string, substrings):
    ''' Determines if a string has any of the substrings listed '''
    for substr in substrings:
        if substr in string:
            return True
    return False
    

def find(params="", look_in=False):
    ''' Find the item that was searched for with necessary paramenters '''
    
    home = look_in if look_in else "~"
    
    avoiders = [
        "Library",
        "Cache",
        ".log",
        ".properties",
    ]
    
    command = 'mdfind -onlyin {}/ "{}"'.format(home.strip("\n"), params)
    
    results = paul.run_script(command, response=True).split("\n")[:-1]
    filtered_results = sorted([line.strip() for line in results 
                    if not has_one_of_substrings(line.strip(), avoiders)], key=len)
    paul.log("RESULTS FIRST 5: ", filtered_results[:10])
    
    if len(filtered_results) > 0:
        if len(filtered_results) > 1:
            decision = choose(filtered_results[:5])
        else:
            decision = filtered_results[0]
        paul.log("DECISION: " + str(decision))
        it = paul.set_it(decision)
        paul.log('IT: {}'.format(it))
        return decision
    else:
        return None



def generate_filters(keywords, prepositions):
    ''' Generate the list of parameters to be used in the search '''
    
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
        if prepositions != None:
            fltr = has_position(prepositions, position - 1)
        else:
            fltr = None
        if fltr:
            params_list.append(filters[fltr].format(
                                filters.get(word, word)))
        else:
            params_list.append(filters.get(word, word))
    
    return params_list


def get(location):
    ''' Open the location '''
    
    if location:
        message = "Opening it."
        paul.run_script('open "{}"'.format(location))
        return message.format(location)
    else:
         return "I couldn't find anything."


def reveal(location):
    ''' Show the location in the Finder '''
    
    if location:
        message = "I found something..."
        paul.run_script('tell application "Finder" to '
                        'reveal POSIX file "{}"'.format(location), 
                        language="applescript")
        return message.format(location)
    else:
         return "I couldn't find anything."


def show_all(query):
    ''' Open the finder with a search done '''
    script = ('tell application "Finder" to activate\n'
    + 'tell application "System Events"\n'
    + '\tkeystroke "n" using {command down}\n'
    + '\tkeystroke "f" using {command down}\n'
    + '\tkey code 48 using {control down, shift down}\n'
    + '\tkeystroke "w" using {command down}\n'
    + '\tkeystroke "' + query + '"\n'
    + '\tkey code 36\nend tell')
    paul.run_script(script, language='applescript')
    return "Here, try these..."


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
        'search': lambda location: reveal(location),
        'reveal': lambda location: reveal(location),
        'locate': lambda location: reveal(location),
        'be': lambda location: reveal(location), # Catch in case, use safer reveal than get
    }
    
    types = {
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
    
    apps = ["app", "application", "program", "executable"]
    
    replaced = sentence.replace_it()
    preps = sentence.get_part("PP", indexes=True)
    paul.log(preps)
    preps = paul.filter_out(preps, "for")
    paul.log(preps)
    
    try:
        object = sentence.get_part("NO")[0]
    except:
        object = None
    verb = sentence.get_part("VB")[0]
    
    if replaced:
        return commands[verb](replaced)
    
    ignore = list(types.keys()) + list(commands.keys())
    
    keywords = sentence.keywords(ignore=["file"])
    paul.log("KEYWORDS: " + str(keywords))
    if keywords == []:
        return "I don't understand. Sorry."
    
    filters = generate_filters(keywords, preps)
    if object in types.keys():
        filters.append("kind:{}".format(types[object]))
    
    if object in apps:
        where = "/Applications"
        params = keywords[0][0] + " kind:application"
        paul.log("FINDING APP")
    else:
        where = False
        params = " ".join(filters)
        paul.log("PARAMETERS: " + str(params))
    
    search = filters[0]
    paul.log(search)
    
    if search.startswith("http") or search.startswith("www."):
        s = search
        paul.open_URL(s if s.startswith("http") else "http://"+s)
        return "Opening the website..."
    elif paul.has_word(keywords, "all"):
        return show_all(params)
    else:
        return commands[verb](find(params, where))


def main():
    ''' The main function '''

    words = {word: ("finder", "noun") for word in NOUNS}
    words.update({word: ("finder", "verb") for word in VERBS})
    
    paul.associate(words)
    paul.register("finder", process)

main()