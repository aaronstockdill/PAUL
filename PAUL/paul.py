"""
paul.py
Author: Aaron Stockdill

The plan is for this to become the main API for building PAUL modules, rather
than importing rather odd things like "brain2" or "user_info" for no apparent
reason. Hopefully this will take care of that! It will also hopefully make
development easier on my part by keeping everything in more logical places.
"""

import random
import time
import itertools
import os
import subprocess
import operator
import urllib.request

import vocab
import Settings.system as system


def log(*to_log):
    ''' Log some info to log.txt if LOGGING, and print it on the screen if
        VERBOSE is True. Any argument that can be converted to a string
        through str() is valid. Returns True if LOGGING is on, False
        otherwise. '''
    return_value = False
    log_string = ' '.join([str(log) for log in to_log])
    if system.flags["LOGGING"]:
        log_file = open("./PAUL/log.txt", 'r')
        lines = log_file.readlines()
        log_file.close()
        max_len = int(system.flags["MAX_LOG_SIZE"])
        time_str = time.strftime("%a,%d-%b-%Y~%H:%M ")
        lines.append(time_str + log_string + "\n")
        if len(lines) < max_len:
            log_file = open("./PAUL/log.txt", 'a')
            log_file.write(lines[-1])
        else:
            log_file = open("./PAUL/log.txt", 'w')
            log_file.write("".join(lines[-max_len:]))
        log_file.close()
        return_value = True
    if system.flags["VERBOSE"]:
        print(log_string)
    return return_value



def update_words():
    """ Add all the new nouns and verbs from the modules. This should 
        never be called explicitly, let Paul handle it. No arguments,
        no return. """

    for word, values in vocab.word_associations.items():
        for _, pos in values:
            if pos == "verb":
                vocab.vocabulary.update({word: vocab.Verb(word),})
            elif pos == "noun":
                vocab.vocabulary.update({word: vocab.Noun(word),})

    vocab.create_irregulars()
    vocab.generate_transforms()
    vocab.create_ordinals()



def associate(words_dict):
    ''' Add this words_dict to the associations list. Argument is a
        dictionary with the word as key, and an info tuple with Module
        and Word_type strings. '''

    for word, info in words_dict.items():
        old = vocab.word_associations.get(word, [])
        vocab.word_associations[word] = old + [info]



def register(module, function):
    ''' Register your module into Paul, providing your module name and the
        function you will use to process the sentences you are passed. '''
    try:
        vocab.word_actions[module] = function
        log("Successfully imported Modules." + module)
        return True
    except:
        log("An error has occured in registering", module)
        return False



def simple_speech_filter(statement):
    ''' Replace a couple of common "error spots" such as °C to degrees
        celcius. Takes in a string, returns a string with replacements.
        You should never need to call this. '''
    replacements = [("°C", " degrees celcius")]
    for find, rep in replacements:
        statement = statement.replace(find, rep)
    return statement    
    


def interact(statement, response=None, end=True):
    """ Standard function for interacting with the user. Use this function,
        not anything custom if possible. 'Response' can be 'list', 'y_n',
        'arb' or None. Statement is whatever you want to ask the user, as
        a string. The return will vary based on the 'response' parameter.
        If 'None', no return. If 'list', an integer relating to the choice
        is returned. If 'arb', the raw string is returned. if 'y_n', True if
        an affirmative, False if negative, None otherwise. """
    
    send = system.flags["SEND"]
    get = system.flags["GET"]
    
    log("INTERACTION:", statement)
    print(statement)
    if system.flags["NOISY"]:
        speech = simple_speech_filter(statement)
        subprocess.Popen('say "{}"'.format(speech), shell=True)
    if send:
        log("CONNECTION: " + repr(send))
        try:
            send(statement, end=end)
        except TypeError:
            send(statement)
    if response:
        if not send:
            bringback = input(system.flags["USER"]["prompt"] + " ")
        else:
            bringback = get()
        negatives = ['no', 'nope']
        positives = ['yes', 'yep', 'yeah']

        if response.split()[0] == 'list':
            ordinal = parse_number(bringback)
            if ordinal:
                log("ORDINAL:", str(ordinal) + ",", bringback)
                return int(ordinal)
            else:
                return None

        elif response == 'y_n':
            if bringback.lower() in negatives:
                return False
            elif bringback.lower() in positives:
                return True
            else:
                return None

        elif response == 'arb':
            return bringback
    
    return statement


def random_choice(list):
    ''' Return one of the supplied statements in list, each of which can
        have room for a name to be inserted into it. '''
    name = random.choice(['', 
            ', {}'.format(get_user_name()),
            ', {}'.format(get_user_title())])
    return random.choice(list).format(name)



def loading():
    ''' Let the user know that Paul is working. Returns what was said
        in case it matters. No arguments. '''
    acknowledgements = [
        "Just a moment{}.",
        "Hang on{}...",
        "Coming up{}.",
        "Let me see{}...",
    ]
    result = random_choice(acknowledgements)
    interact(result, end=False)
    return result



def acknowledge(end=False):
    ''' Simply acknowledge the user, without any real thought into the
        respose. Returns what was said, incase it matters. Optional end
        argument, defaults to False, setting whether you are done interating
        with the user. With default end=False, is it assumed you will then 
        provide the user with more information. '''

    acknowledgements = [
        "Ok{}.",
        "Sure{}.",
        "Of course{}.",
        "Certainly{}.",
    ]
    result = random_choice(acknowledgements)
    interact(result, end=end)
    return result



def iterable(item):
    ''' Determine if the item in question is iterable. Argument is an object.
        Returns true if is is, false otherwise. '''
    return type(item) in [list, tuple, dict, Sentence]



def trim_word(word_list, word, toplevel=True):
    ''' Remove the word from a list -- useful if you know the likes
        of keywords will return a word you'd rather not get. 
        Arguments are word_list, the list/tuple/whatever of words; and word,
        the word that should be removed. If it is part of a sublist/tuple
        the whole sublist/tuple is removed. No return. '''
    for item in word_list:
        if not iterable(item):
            if item == word:
                if toplevel:
                    word_list.remove(item)
                else:
                    return True
                break
        else:
            remove = trim_word(item, word, toplevel=False)
            if remove:
                word_list.remove(item)


def has_word(word_list, word):
    ''' Find if the desired word is in the list, e.g. is 'cat' in the 
        list 'keywords'. Arguments are the word_list to be searched, and
        the word you are looking for. Returns True if found, False 
        otherwise '''
    for item in word_list:
        if not iterable(item):
            if type(item) == str and word in item.split():
                return True
        else:
            found = has_word(item, word)
            if found:
                return True
    return False



def has_one_of(list_to_search, confirm_list):
    ''' Given a list of words, is one of the items in confirm_list in it?
        Two lists are the arguments: list_to_search, which is the list of
        words that you hope to find something in; and confirm_list, which
        is the list with the words you are hoping to find one of in
        list_to_search. Returns True if one or more words is found, False
        otherwise. Shortcuts as necessary. '''
    for word in confirm_list:
        if has_word(list_to_search, word):
            return True
    return False



def join_lists(*lists):
    ''' Joins the lists. Arguments are lists that get joined, but are 
        quitely ignored if not a list. The newly created list is returned. '''

    connected = []
    for item in lists:
        if isinstance(item, list):
            connected += item
    return connected


def filter_unless_listed(main_list, *rest):
    ''' Given a main list, filter any words not in the other lists from it.
        Arguments are the main_list that you are filtering, and any lists
        of words that need to be retained. Returns the main_list with only
        the words in the other lists. '''
    return_list = []
    comparative = join_lists(*rest)
    for item in main_list:
        if iterable(item):
            if has_one_of(item, comparative):
                return_list.append(item)
        elif item in comparative:
            return_list.append(item)
    return return_list



def filter_out(main_list, *rest):
    ''' Filter any item from the main list that is found in the rest.
        Arguments are a main_list that you are filtering, and any lists
        with words that you want to remove from the main_list. Returns
        the main_list without the words in the other lists. '''
    return_list = []
    for item in main_list:
        comparative = join_lists(*rest)
        if iterable(item):
            if not has_one_of(item, comparative):
                return_list.append(item)
        elif item not in comparative:
            return_list.append(item)
    return return_list



def run_script(code, language='bash', response=False):
    ''' Run the code provided. Defaults to bash, can also be
        applescript, python3, ruby or perl. One-liners are recommended for
        python3, perl and ruby. Response determines if a response is required
        from the code. The response is the returned value. '''
    
    if language == "applescript":
        code = 'osascript -e "{}"'.format(code.replace("\"", "\\\""))
    elif language == "python3":
        code = 'python3 -c "{}"'.format(code.repace("\"", "\\\""))
    elif language == "ruby":
        code = 'ruby -e "{}"'.format(code.repace("\"", "\\\""))
    elif language == "perl":
        code = 'perl -e "{}"'.format(code.repace("\"", "\\\""))
    log("CODE:", code)
    if not system.flags["EXEC"]:
        if response == False:
            os.popen(code)
            return None
        else:
            return os.popen(code).read()
    else:
        data = system.flags["EXEC"](code, response)
        return data



def open_URL(url):
    ''' Open the url that was passed in as a string. Returns True if 
        successful, False otherwise. '''
    log("OPENING URL: ", url)
    try:
        run_script('open "{}"'.format(url), language="bash")
        return True
    except:
        log("OPEN_URL FAILED TO OPEN {}".format(url))
        return False



def set_it(value):
    ''' Sets the global value of "it" to the given value. Return the 
        new value, explicitly from "it", in case verification is needed. '''
    system.flags["IT"] = value
    return system.flags["IT"]



def get_it():
    ''' To get "it". No arguments, returns the "it" value. '''
    return system.flags["IT"]



def get_version():
    ''' Returns the current version of Paul as a string '''
    return system.flags["VERSION"]



def get_user_name():
    ''' Returns the name of the current user as a string. '''
    return system.flags["USER"]["name"]



def get_user_title():
    ''' Returns the title of the current user as a string. '''
    return system.flags["USER"]["title"]



def get_woeid():
    ''' Return the woeid of the current user, as a string. '''
    return system.flags["USER"]["woeid"]



def get_temp():
    ''' Return either C or F, denoting the user's temperature preference. '''
    return system.flags["USER"]["temp"]



def get_search_engine():
    ''' Return the name of the user's search engine, as a string. '''
    return system.flags["USER"]["search_engine"]



def get_prompt():
    ''' Return the user's prompt as a string. '''
    return system.flags["USER"]["prompt"]



def send_notification(title, message):
    ''' Send the user a notification using the system notifications
        with a title and message as the arguments. No return. '''
    notification = ('display' + 
    ' notification "{}" with title "PAUL" subtitle "{}"'.format(
        message, title
    ))
    run_script(notification, language='applescript')



def parse_number(string):
    ''' Attempt to parse a number into it's value. Takes a string, 
        returns an integer. If it finds a valid integer, e.g. "42", it
        just returns that, 42. '''
    
    numbers = string.lower().split()

    ones = { 
        "zero": 0, "one": 1, "two": 2, 
        "three": 3, "four": 4, "five": 5, 
        "six": 6, "seven": 7, "eight": 8, "nine": 9,
    }
    ones_ordinals = {
        "zeroth": 0, "first": 1, "second": 2,
        "third": 3, "fourth": 4, "fifth": 5,
        "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9,
    }
    teens = { 
        "eleven": 11, "twelve": 12, "thirteen": 13, 
        "fourteen": 14, "fifteen": 15, "sixteen": 16, 
        "seventeen": 17, "eighteen": 18, "nineteen": 19,
    }
    teens_ordinals = {
        "twelfth": 12,
    }
    tens = {
        "ten": 10, "twenty": 20, "thirty": 30, 
        "forty": 40, "fifty": 50, "sixty": 60, 
        "seventy": 70, "eighty": 80, "ninety": 90,
    }
    multipliers = {
        "hundred": 100, "thousand": 1000, "million": 1000000, 
        "billion": 1000000000, "trillion": 1000000000000,
    }

    if numbers[0] in multipliers:
        numbers = ["one"] + numbers

    number = 0
    for word in numbers:
        if word in ones:
            number += ones[word]
            if numbers[numbers.index(word)+1] not in multipliers:
                return number
        elif word in ones_ordinals:
            number += ones_ordinals[word]
            if numbers[numbers.index(word)+1] not in multipliers:
                return number
        elif word in teens:
            number += teens[word]
            if numbers[numbers.index(word)+1] not in multipliers:
                return number
        elif word[:-2] in teens:
            number += teens[word[:-2]]
            if numbers[numbers.index(word)+1] not in multipliers:
                return number
        elif word in teens_ordinals:
            number += teens_ordinals[word]
            if numbers[numbers.index(word)+1] not in multipliers:
                return number
        elif word in tens:
            number += tens[word]
        elif word[:-4]+"y" in tens:
            number += tens[word[:-4]+"y"]
            return number
        elif word in multipliers:
            number *= multipliers[word]
        elif word[:-2] in multipliers:
            number *= multipliers[word[:-2]]
            return number
        else:
            try:
                x = int(word)
                log("FOUND INT: ", x)
                return x
            except ValueError:
                log("INT PARSE IGNORING", word)

    return number



class Sentence(object):
    ''' This is the sentence object to contain all the methods needed
        when working with them. Only initialization argument is the sentence
        string. '''

    def __init__(self, init_string):
        ''' Creates the sentence that is used for all the code, as well
            as some other variables.

            >>> s = Sentence("This is a doctest.")

            >>> s = Sentence(42)
            Traceback (most recent call last):
                ...
            TypeError: init_string must be a string
        '''


        if type(init_string) != str:
            raise TypeError("init_string must be a string")

        words = [self.clean(word) for word
                 in init_string.strip().lower().split(' ')]
        self.sentence_string = " ".join(words)
        self.sentence = self.tag_sentence(words)
        self.kind = self.classify()


    def __repr__(self):
        ''' Reveal how the sentence is thought of in Python

            >>> Sentence("This is a doctest.")
            [('this', 'PS'), ('be', 'VB'), ('the', 'AR'), ('doctest', '??')]
        '''
        return str(self.sentence)


    def __str__(self):
        ''' A 'pretty' representation of the sentence.

            >>> print(Sentence("This is a doctest."))
            this is a doctest
        '''
        return self.sentence_string


    def __iter__(self):
        ''' For iterating over the words in the sentence. '''
        return iter(self.sentence)


    def keywords(self, ignore=None, include=None):
        ''' Join things not split by prepositions and stuff, as they probably
            "belong" together. Ignore certain words by putting them in the
            ignore list. Include a certain type of word by listing the types
            in include. By default, keywords gets ?? (unknowns), NO (objects)
            and XO (names).
        '''

        if ignore is None:
            ignore = []

        objects = self.get_part("NO", indexes=True)
        names = self.get_part("XO", indexes=True)
        numbers = self.get_part("NU", indexes=True)
        keywords = self.get_part("??", indexes=True)

        if include is not None:
            other = []
            for key in include:
                part = self.get_part(key, indexes=True)
                if part:
                    other = other + part
        else:
            other = None

        new_items = [(i, j) for i, j in join_lists(objects,
                                                   names,
                                                   numbers,
                                                   keywords,
                                                   other)
                                        if i not in ignore]

        item_list = []
        iterhelper = lambda i: i[0]-i[1][1]
        for _, item in itertools.groupby(enumerate(new_items), iterhelper):
            final_items = (list(map(operator.itemgetter(1), item)))
            ind = final_items[0][1]
            final_items = ' '.join([item[0] for item in final_items])
            item_list.append((final_items, ind))

        keyword_list = sorted(item_list, key=lambda i: i[1])
        return keyword_list



    def get_part(self, part, indexes=False, pronouns=False):
        ''' Return the objects in a sentence of type 'part', or None.
            Set indexes if you want the index of the word in the sentence,
            and pronouns if pronouns can be included in the sentence. If
            nothing is found without pronouns, it tries again with pronouns
            anyway. If there is still nothing, it returns None.
        '''

        if part == "NO" or part == "XO":
            if pronouns:
                part = [part, "PO"]
            else:
                part = [part]
        elif part == "NS" or part == "XS":
            if pronouns:
                part = [part, "PS"]
            else:
                part = [part]
        else:
            part = [part]

        if not indexes:
            parts = [word[0] for word in self.sentence if word[1] in part]
        else:
            parts = [(word[0], self.sentence.index(word))
                     for word in self.sentence if word[1] in part]
        if len(parts) > 0:
            return parts
        elif not pronouns:
            return self.get_part(part, pronouns=True)
        else:
            return None


    def clean(self, word):
        ''' Clean the text, removing unwanted characters '''

        for to_remove in list(" ,.?'\";:\\!$&<>@#%}{[]_"):
            word = word.strip(to_remove)
        return word


    def tag_word(self, word):
        """ Tag the word's part of speech, returning the word's base and tag
            in a tuple. """

        if word not in vocab.vocabulary:
            return (word, "??")
        else:
            return (vocab.vocabulary[word].base, vocab.vocabulary[word].tag())


    def classify(self):
        ''' Determines what the concept of the sentence is.
            Can be declarative (DEC), Interrogative (INT),
            or Imperative (IMP). Largly obsolete. '''

        if (self.sentence[0][1] == "VB" or
            self.sentence[0][0] == "paul"):
            kind = "IMP"
            self.sentence.insert(0, ("You", "PS"))
        elif self.sentence[0][1] == "WH":
            kind = "INT"
        else:
            kind = "DEC"
        return kind


    def tag_sentence(self, words):
        ''' Tag all the words in a sentence, applying various rules as
            necessary to fix up 'oddities'. '''

        sentence = []
        verb_index = 999999
        object_index = 999999
        add_are = False
        for i in range(len(words)):
            word = words[i]
            if word[-3:] == "'re":
                base, part = self.tag_word(word[:-3])
                add_are = True
            else:
                base, part = self.tag_word(word)
            if part == "WH" and word[-2:] == "'s":
                sentence.append((base, part))
                sentence.append(("be", "VB"))
                verb_index = i
            elif word in ["it", "that"]:
                sentence.append(("it", "PO"))
            elif word == "i'm":
                sentence += [("i", "NS"), ("be", "VB")]
            elif part in ["N", "P", "X"]:
                if i < verb_index:
                    part = part + "S"
                else:
                    part = part + "O"
                    object_index = i
                sentence.append((base, part))
            elif part == "VB":
                if i < object_index:
                    verb_index = i
                else:
                    part = "PP"
                    base = vocab.vocabulary[word].past()
                sentence.append((base, part))
            else:
                sentence.append((base, part))
            if add_are:
                sentence.append(("be", "VB"))
                add_are = False
        return sentence



    def replace_it(self):
        ''' Replace 'it' or 'that' with the current global concept. Returns
            what 'it' is if a replacement was made, False otherwise. '''

        for i, word in enumerate(self.sentence):
            if word[0] == 'it':
                it = get_it()
                log("IT:", str(it))
                if it == None:
                    return False
                self.sentence.pop(i)
                self.sentence.insert(i, (it, "XO"))
                return it
        return False



    def forward(self, module):
        ''' Forward sentence to the module specified.
            Returns the new result of successful, else False. '''
        
        log("FORWADING TO:", module)
        if module in vocab.word_actions.keys():
            return vocab.word_actions[module](self)
        else:
            return False
    
    
    def has_word(self, word):
        ''' The sentence object's version of paul.has_word, where the assumed
            list of words is the sentence. '''
        return has_word(self.sentence, word)
    
    
    def has_one_of(self, confirm_list):
        ''' The sentence object's version of paul.has_one_of, where the
            assumed list of words is the sentence. '''
        return has_one_of(self.sentence, confirm_list)


class Element(object):
    ''' A simple element object for the DOM parser '''
    
    def __init__(self, tag_code):
        ''' Initialise with tag name and attributes '''
        self.code = tag_code
        self.tag = self.get_name()
        self.children = []
        self.attributes = self.get_attributes()
    
    def __str__(self):
        return "({}, {})".format(self.tag, str(self.children))
    
    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, i):
        ''' Get item via slice notation, changes based on input '''
        if type(i) == int:
            return self.children[i]
        elif i[0] == "#":
            return self.get_id(i[1:])
        elif i[0] == ".":
            c = self.get_class(i[1:])
            return c if c != [] else None
        else:
            return self.get_elem(i)
    
    
    def get_id(self, target):
        ''' Get the element with id "target" recursively, return 
            the first suitable element '''
        if self.attributes.get("id", None) == target:
            return self
        else:
            for c in self.children:
                try:
                    e = c['#{}'.format(target)]
                    if e:
                        return e
                except TypeError:
                    pass
        return None
    
    def get_class(self, target):
        ''' Get the elements with class "target" recursively, return 
            a list of suitable elements '''
        result = []
        if self.attributes.get("class", None) == target:
            result += [self]
        for c in self.children:
            try:
                e = c['.{}'.format(target)]
                if e:
                    result += e
            except TypeError:
                pass
        return result
    
    def get_elem(self, target):
        ''' Get the element "target" recursively, return a list of suitable
            elements '''
        result = []
        if self.tag == target:
            result += [self]
        for c in self.children:
            try:
                e = c['{}'.format(target)]
                if e:
                    result += e
            except TypeError:
                pass
        return result
    
    def get_name(self):
        ''' Try and get the name of the tag '''
        try:
            return self.code.split()[0][1:].lower().strip(">")
        except IndexError:
            print ("'{}'".format(self.code))
    
    def get_parts(self, string):
        ''' Extract the parts of the element tag, the attributes. '''
        parts = {}
        key = ""
        value = ""
        encloser = None
        for char in string.strip():
            if char == "=":
                key = value
                value = ""
            elif char == "'":
                if encloser == "'":
                    parts[key] = value
                    encloser = None
                    key = ""
                    value = ""
                elif encloser:
                    value += char
                else:
                    encloser = "'"
            elif char == '"':
                if encloser == '"':
                    parts[key] = value
                    encloser = None
                    key = ""
                    value = ""
                elif encloser:
                    value += char
                else:
                    encloser = '"'
            elif char == " ":
                if encloser:
                    value += char
                elif key != "":
                    parts[key] = value
                    key = ""
                    value = ""
                else:
                    parts[key] = value
                    key = ""
                    value = ""
            else:
                value += char
        try:
            del parts[""]
        except KeyError:
            pass
        return parts
    
    def get_attributes(self):
        ''' Try and get attributes of element, e.g. id and class '''
        c = self.code.strip().strip(">").strip("<")
        c = " ".join(c.split()[1:])
        parts = self.get_parts(c)
        return parts
    
    def get_immediate_child(self, target):
        ''' Useful if you only want immediate children of an element,
            not EVERY child of an element. '''
        if target[0] == "#":
            for c in self.children:
                try:
                    if c.attributes["id"] == target[1:]:
                        return c
                except TypeError:
                    pass
        elif target[0] == ".":
            result = []
            for c in self.children:
                try:
                    if c.attributes["class"] == target[1:]:
                        result += [c]
                except TypeError:
                    pass
            return result
        else:
            result = []
            for c in self.children:
                try:
                    if c.tag == target:
                        result += [c]
                except AttributeError:
                    pass
            return result
    
    def extract_raw_text(self):
        ''' Extract out raw text, so there are no tags or anything. '''
        out = ""
        for c in self.children:
            if type(c) == Element:
                out += c.extract_raw_text()
            else:
                out += c
        return out



class DOM(object):
    ''' Create a DOM, and work with it. Useful to parse HTML '''
    
    def __init__(self, html):
        ''' Create the DOM from the html '''
        self.code = html
        self.tokens = self.tokenize(html)
        self.dom = self.domify(self.tokens)
        
    @classmethod
    def fromURL(self, url):
        ''' Create a new DOM object from a given URL '''
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent',
                              'PAUL/{}'.format(get_version()))]
        infile = opener.open(url)
        page = str(infile.read(), encoding='utf8')
        newDOM = DOM(page)
        return newDOM
    
    def __getitem__(self, key):
        ''' Nice access straight to the DOM. '''
        return self.dom[key]
    
    def __str__(self):
        ''' Pretty-print DOM '''
        return str(self.dom)
    
    def remove_non_html(self, tokens):
        ''' Remove scripts and styles '''
        cont = True
        j = 0
        new_tokens = []
        while cont:
            tag = tokens[j]
            try:
                tag_name = tag.split()[0].strip(">").strip("<")
            except:
                tag_name = "  "
            if tag_name in ["style", "script"]:
                cont2 = True
                if tag_name == "script" and tag[-2:] == "/>":
                    pass # Ignore it
                else:
                    while cont2:
                        try:
                            tag_name2 = tag.split()[0].strip(">").strip("<").strip("/")
                        except:
                            tag_name2 = "  "
                        if tag_name2 == tag_name:
                            cont2 = False
                        j += 1
            else:
                if not (tag in ["</style>", "</script>"]):
                    new_tokens.append(tag)
            j += 1
            if j == len(tokens):
                cont = False
        return new_tokens
    
    def tokenize(self, code):
        ''' Turn the code into tokens '''
        tokens = []
        i = 0
        for char in code:
            if char == "\n":
                pass
            elif char == ">":
                tokens[i] += char
                i += 1
            elif char == "<":
                if (i+1) == len(tokens):
                    i +=1
                tokens.append(char)
            else:
                try:
                    tokens[i] += char
                except IndexError:
                    tokens.append(char)
        
        return self.remove_non_html(tokens)
    
    
    def domify(self, tokens):
        ''' Parse the tokens into a DOM. '''
        
        def in_stack(tag, stack):
            for i in stack:
                if type(i) == str:
                    try:
                        if i.split()[0][1:] == tag or i.split()[0][1:-1] == tag:
                            return True
                    except IndexError:
                        pass
            return False
        
        stack = []
        detag = lambda a: a.split()[0].strip("<").strip(">")
        for t in tokens:
            try:
                tag_name = detag(t)
                tag_end = t[-2:]
            except:
                stack.append(t)
                continue
            if tag_name == "!DOCTYPE":
                pass
            elif tag_end == "/>":
                e = Element(t)
                stack.append(e)
            elif len(t) > 1 and t[1] == "/":
                alt = t[2:-1]
                if in_stack(alt, stack):
                    temp = []
                    cont = True
                    while cont:
                        try:
                            if (type(stack[-1]) == str):
                                if stack[-1].strip() == "":
                                    temp.append(" ")
                                    stack.pop()
                                elif detag(stack[-1]) == alt:
                                    cont = False
                                elif stack[-1][0] == "<" and stack[-1][-1] == ">" and detag(stack[-1]) != alt:
                                    temp.append(stack.pop())
                                    n = self.domify(temp)
                                    temp.append(n)
                                else:
                                    temp.append(stack.pop())
                                    # cont = False
                            else:
                                temp.append(stack.pop())
                        except IndexError:
                            cont = False
                    try:
                        tag = stack.pop()
                    except IndexError:
                        pass
                    temp.reverse()
                    e = Element(tag)
                    e.children = temp
                    stack.append(e)
            else:
                stack.append(t)
        return stack[0]

update_words()