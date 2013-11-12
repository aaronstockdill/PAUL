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

import vocab
import user_info


def log(*to_log):
    ''' Log some info to log.txt, and print it on the screen if
        VERBOSE is True '''
    if user_info.flags["LOGGING"]:
        log_string = ' '.join([str(log) for log in to_log])
        log_file = open("./PAUL/log.txt", 'r')
        lines = log_file.readlines()
        log_file.close()
        max_len = user_info.flags["MAX_LOG_SIZE"]
        time_str = time.strftime("%a,%d-%b-%Y~%H:%M ")
        lines.append(time_str + log_string + "\n")
        if len(lines) < max_len:
            log_file = open("./PAUL/log.txt", 'a')
            log_file.write(lines[-1])
            log_file.close()
        else:
            log_file = open("./PAUL/log.txt", 'w')
            log_file.write("".join(lines[1:]))
            log_file.close()
    if user_info.flags["VERBOSE"]:
        print(log_string)



def update_words():
    """ Add all the new nouns and verbs from the modules """

    for word, values in vocab.word_associations.items():
        for _, pos in values:
            if pos == "verb":
                vocab.vocabulary.update({word: vocab.Verb(word),})
            elif pos == "noun":
                vocab.vocabulary.update({word: vocab.Noun(word),})

    vocab.create_irregulars()
    vocab.generate_transforms()



def associate(words_dict):
    ''' Add this words_dict to the associations list '''

    for word, info in words_dict.items():
        old = vocab.word_associations.get(word, [])
        vocab.word_associations[word] = old + [info]



def get_client_data():
    ''' Get some response from the client. '''
    done = False
    result = ""
    user_info.flags["SERVER"].send(bytes(" "*1024, "utf-8"))
    while not done:
        come_back = user_info.flags["SERVER"].recv(1024)
        info = str(come_back, "utf-8").strip()
        log("RECIEVING:", info)
        if info == "client_done":
            log("DONE RECIEVING")
            done = True
        else:
            result += info
    log("RESULT:", result)
    return result



def simple_speech_filter(statement):
    ''' Replace a couple of common "error spots" such as °C to 
        degrees celcius '''
    statement = statement.replace("°C", " degrees celcius")
    return statement
    
    


def interact(statement, response=None):
    """ Standard function for interacting with the user. Use this function,
        not anything custom if possible. 'Response' can be 'list', 'y_n', 'arb'
        or None """
    
    s = user_info.flags["SERVER"]
    def send(phrase):
        s.send(bytes(" "*1024, "utf-8"))
        s.send(bytes(phrase, 'utf-8'))
        s.send(bytes(" "*1024, "utf-8"))
    
    log("INTERACTION:", statement)
    print(statement)
    if user_info.flags["NOISY"]:
        speech = simple_speech_filter(statement)
        subprocess.Popen('say "{}"'.format(speech), shell=True)
    if s:
        log("CONNECTION: " + repr(s))
        send(statement)
    if response:
        if not user_info.flags["SERVER"]:
            bringback = input(user_info.info["prompt"] + " ")
        else:
            send("paul_done")
            bringback = get_client_data()
        numbers = {
            '1': "first",
            '2': "second",
            '3': "third",
            '4': "fourth",
            '5': "fifth",
        }
        if bringback in numbers.keys():
            bringback = Sentence(numbers[bringback])
        else:
            bringback = Sentence(bringback)
        ordinal = bringback.get_part("OR")
        negatives = ['no', 'nope']
        positives = ['yes', 'yep', 'yeah']

        if response == 'list':
            if ordinal:
                log("ORDINALS: " + str(ordinal))
                int_version = vocab.vocabulary[ordinal[0]]['value']
                return int_version
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
            return bringback.lower()

    return statement



def loading():
    ''' Let the user know that Paul is working. Returns what was said
        incase it matters. '''
    name = random.choice(['', ', {}'.format(user_info.info['name'])])
    acknowledgements = [
        "Just a moment{}.".format(name),
        "Hang on{}...".format(name),
        "Coming up{}.".format(name),
        "Let me see{}...".format(name),
    ]
    result = random.choice(acknowledgements)
    interact(result)
    return result



def acknowledge():
    ''' Simply acknowledge the user, without any real thought into
        the respose. Returns what was said, incase it matters. '''

    name = random.choice(['', ', {}'.format(user_info.info['name'])])
    acknowledgements = [
        "Ok{}.".format(name),
        "Sure{}.".format(name),
        "Of course{}.".format(name),
        "Certainly{}.".format(name),
    ]
    result = random.choice(acknowledgements)
    interact(result, done_interacting = False)
    return result



def iterable(item):
    ''' Determine if the item in question is iterable '''
    return type(item) in [list, tuple, dict]



def trim_word(wordlist, word, toplevel=True):
    ''' Remove the word from a list -- useful if you know the likes
        of keywords will return a word you'd rather not get. '''
    for item in wordlist:
        if not iterable(item):
            if item == word:
                if toplevel:
                    wordlist.remove(item)
                else:
                    return True
                break
        else:
            remove = trim_word(item, word, toplevel=False)
            if remove:
                wordlist.remove(item)


def has_word(word_list, word):
    ''' Find if the desired word is in the list,
        e.g. is 'cat' in the list 'keywords' '''
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
    ''' Given a list of words, is one of the items in confirm_list in it? '''
    for word in confirm_list:
        if has_word(list_to_search, word):
            return True
    return False



def join_lists(*lists):
    ''' Joins the lists, but only if they exist.
        If one of the values is none, it isn't added. '''

    connected = []
    for item in lists:
        if item:
            connected += item

    return connected


def filter_unless_listed(main_list, *rest):
    ''' Given a main list, filter any words not in the other lists from it '''
    return_list = []
    for item in main_list:
        comparative = join_lists(*rest)
        if iterable(item):
            if has_one_of(item, comparative):
                return_list.append(item)
        elif item in comparative:
            return_list.append(item)
    return return_list



def filter_out(main_list, *rest):
    ''' Filter any item from the main list that is found in the rest '''
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
    ''' Run the script code provided. Defaults to bash, can also be applescript
        or python3. '''
    
    if language == "applescript":
        code = 'osascript -e "{}"'.format(code.replace("\"", "\\\""))
    elif language == "python3":
        code = "python {}".format(code)
    log("CODE:", code)
    if not user_info.flags["SERVER"]:
        return os.popen(code).read()
    else:
        user_info.flags["SERVER"].send(bytes(1024*" ", "utf-8"))
        user_info.flags["SERVER"].send(bytes("SCRIPT{}SCRIPT".format(code), "utf-8"))
        user_info.flags["SERVER"].send(bytes(1024*" ", "utf-8"))
        data = get_client_data()
        return data



def set_it(value):
    ''' Sets the global value of "it" to the given value. Return the 
        new value, explicitly from it, incase verification is needed. '''
    user_info.info["it"] = value
    return user_info.info["it"]



def send_notification(title, message):
    ''' Send the user a notification using the system notifications
        with a title and message '''
    notification = ('display' + 
    ' notification "{}" with title "PAUL" subtitle "{}"'.format(
        message, title
    ))
    run_script(notification, language='applescript')



class Sentence(object):
    ''' This is the sentence object to contain all the methods needed
        when working with them '''

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
        self.keyword_list = None


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
        return iter(self.sentence)


    def keywords(self, ignore=None, include=None):
        ''' Join things not split by prepositions and stuff, as they probably
            "belong" together. Ignore certain words by putting them in the
            ignore list. Include a certain type of word by listing the types
            in include. By default, keywords gets ?? (unknowns), NO (objects) and XO (names).
        '''

        if ignore is None:
            ignore = []

        objects = self.get_part("NO", indexes=True)
        names = self.get_part("XO", indexes=True)
        ordinals = self.get_part("OR", indexes=True)
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
                                                   ordinals,
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

        self.keyword_list = sorted(item_list,
                                   key=operator.itemgetter(1))
        return self.keyword_list



    def get_part(self, part, indexes=False, prepositions=False):
        ''' Return the objects in a sentence of type part, or None.
            Set indexes if you want the index of the word in the sentence,
            and prepositions if prepositions can be included in the sentence
        '''

        if part == "NO" or part == "XO":
            if prepositions:
                part = [part, "PO"]
            else:
                part = [part]
        elif part == "NS" or part == "XS":
            if prepositions:
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
        elif not prepositions:
            return self.get_part(part, prepositions=True)
        else:
            return None


    def clean(self, word):
        ''' Clean the text, removing unwanted characters '''

        for to_remove in list(" ,.?'\";:\\!$&<>@#%^*}{[]+-=_"):
            word = word.strip(to_remove)
        return word


    def tag_word(self, word):
        """ Tag the word's part of speech, returning the word's base and tag
            in a tuple """

        if word not in vocab.vocabulary:
            return (word, "??")
        else:
            return (vocab.vocabulary[word].base, vocab.vocabulary[word].tag())


    def classify(self):
        ''' Determines what the concept of the sentence is.
            Can be declarative (DEC), Interrogative (INT),
            or Imperative (IMP)'''

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
            necessary to fix up oddities '''

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
        ''' Replace 'it' or 'that' with the current global concept '''

        for i, word in enumerate(self.sentence):
            if word[0] == 'it':
                log("IT:", str(user_info.info['it']))
                if user_info.info['it'] == None:
                    return False
                self.sentence.pop(i)
                self.sentence.insert(i, (user_info.info["it"], "XO"))
                return True
        return False



    def forward(self, module):
        ''' Forward sentence to the module specified.
            Returns True of successful, else False. '''
        log("FORWADING TO:", module)
        if module in vocab.word_actions.keys():
            return vocab.word_actions[module](self)
        else:
            return False
    
    
    def has_word(self, word):
        return has_word(self.sentence, word)


update_words()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
