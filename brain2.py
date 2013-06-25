"""
brain.py
A rewrite of brain.py, this is where the sentence is tagged so it can be
used by the modules more easily, and exactly which module is required is
also decided here. It really is the brain.
Author: Aaron Stockdill
"""

import random
import os
import itertools
import operator

import vocab
import user_info
from Modules.importer import *

class Sentence(object):
    ''' This is the sentence object to contain all the methods needed
        when working with them '''
        
    def __init__(self, sentence_string):
        ''' Creates the sentence that is used for all the code, as well
            as some other variables '''
        
        self.sentence_string = sentence_string.lower()
        words = [self.clean(word) for word in sentence_string.split(' ')]
        self.sentence = self.tag_sentence(words)
        self.kind = self.classify()
        self.keyword_list = None
    
    
    def __repr__(self):
        return self.sentence
    
    
    def __str__(self):
        return self.sentence_string
    
    
    def __iter__(self):
        return iter(self.sentence)
        

    def keywords(self, ignore=[]):
        ''' Join things not split by prepositions and stuff, as they probably
            "belong" together. Ideal for getting keywords. If keywords have 
            been found before, use them rather than trying to find them 
            again. This means if the function is called again and again but
            is not stored in a variable, the performance hit is negligible. '''
        
        if self.keyword_list is not None:
            if user_info.VERBOSE: print("KEYWORDS: Short-circuit successful.")
            return self.keyword_list
        else:
            objects = self.get_parts("NO", True)
            names = self.get_parts("XO", True)
            keywords = self.get_parts("??", True)
    
            all_together = []
    
            if objects:
                all_together += objects
            if names:
                all_together += names
            if keywords:
                all_together += keywords
    
            words = [item[0] for item in all_together if item[0] not in ignore]
            new_items = []
            for word in words:
                word_index = [item[1] for item in all_together 
                              if item[0] == word][0]
                new_items.append((word, word_index))
    
            item_list = []
            iterhelper = lambda i: i[0]-i[1][1]
            for k, g in itertools.groupby(enumerate(new_items), iterhelper):
                final_items = (list(map(operator.itemgetter(1), g)))
                ind = final_items[0][1]
                final_items = ' '.join([item[0] for item in final_items])
                item_list.append((final_items, ind))
    
            final_list = item_list
        
            self.keyword_list = sorted(final_list, key=operator.itemgetter(1))
            return self.keyword_list
    
    
    def group_together(self):
        if user_info.VERBOSE: print("WARNING: use of 'group_together'"
                                    "is deprecated. Use 'keywords' instead.")
        return self.keywords()


    def log_unknown(self, word, options):
        ''' Log the unknown words that we come across,
            and what we think it is '''
    
        file = open("Unknown_words.csv", "a")
        file.write("'{}': {}\n".format(word, options))
        file.close


    def get_parts(self, part, indexes=False, prepositions=False):
        ''' Return the objects in a sentence of type part, or None.
            Set indexes if you want the index of the word in the sentence,
            and prepositions if prepositions can be included in the sentence'''
        
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
            return self.get_parts(part, prepositions=True)
        else:
            return None


    def clean(self, word):
        ''' Clean the text, removing unwanted characters '''
    
        for to_remove in list(" ,.?'\";:\\!$&<>@#%^*{}[]+-=_"):
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
            self.sentence[0][0] == user_info.info["computer"]):
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
        for i in range(len(words)):
            word = words[i]
            base, part = self.tag_word(word)
            if part == "WH" and word[-2:] == "'s":
                    sentence.append((base, part))
                    sentence.append(("be", "VB"))
                    verb_index = i
            elif word in ["it", "that"]:
                sentence.append((user_info.info["it"], "XO"))
                if user_info.VERBOSE: print("IT:", user_info.info['it'])
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
        return sentence
        


def commands(sentence):
    ''' Process a command, based on nouns and verbs in the sentence '''

    subs = sentence.get_parts("NS")
    objs = sentence.get_parts("NO")
    if subs and objs:
        objects = subs + objs
    elif subs:
        objects = subs
    elif objs:
        objects = objs
    else:
        objects = None

    verbs = sentence.get_parts("VB")
    if verbs:
        verb = verbs[0]
    else:
        verb = None

    if objects is not None:
        object_noun = "the {}".format(objects[0])
        if objects[0] in user_info.nouns_association:
            return user_info.nouns_association[objects[0]](sentence)
        else:
            if verb in user_info.verbs_association:
                return user_info.verbs_association[verb](sentence)
    elif verb in user_info.verbs_association:
        object_noun = "it"
        return user_info.verbs_association[verb](sentence)
    discover.process(sentence)
    return "Let me find out for you..."



def interact(statement, response=None):
    """ Standard function for interacting with the user. Use this function,
        not anything custom if possible. Response can be 'list', 'y_n', 
        or None """
    
    print(statement)
    if user_info.NOISY: os.system('say "{}"'.format(statement))
    if response:
        bringback = Sentence(input("> "))
        ordinal = bringback.get_parts("OR")
        declines = ['none', 'neither']
        negatives = ['no', 'nope']
        positives = ['yes', 'yep', 'yeah']
    
        if response == 'list':
            if ordinal:
                if user_info.VERBOSE: print("ORDINALS: ", ordinal)
                return vocab.vocabulary[ordinal[0]]['value']
            elif bringback.lower() in declines:
                return None
            if user_info.VERBOSE: print("NUMBER:", int(bringback))
            return int(bringback)
        
        elif response == 'y_n':
            if bringback.lower() in negatives:
                return False
            elif bringback.lower() in positives:
                return True
            else:
                return None

    return statement



def forward(sentence, keyword):
    ''' If you think you know which module should deal with this instead
        of who brain2 picked, pass it here with a keyword. '''

    if keyword in user_info.nouns_association.keys():
        return user_info.nouns_association[keyword](sentence)
    elif keyword in user_info.verbs_association.keys():
        return user_info.verbs_association[keyword](sentence)
    else:
        return discover.process(sentence)
    


def loading():
    ''' Let the user know that Paul is working '''
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
        the respose '''

    name = random.choice(['', ', {}'.format(user_info.info['name'])])
    acknowledgements = [
        "Ok{}.".format(name),
        "Sure{}.".format(name),
        "Of course{}.".format(name),
        "Certainly{}.".format(name),
    ]
    result = random.choice(acknowledgements)
    interact(result)
    return result
        


def process(line):
    ''' Process the given line '''
    
    sentence = Sentence(line)
    
    if user_info.VERBOSE: print("SENTENCE:", sentence)
    if user_info.VERBOSE: print("KIND:", sentence.kind)
    
    if sentence.kind == "IMP" or sentence.kind == "INT":
        response = commands(sentence)    
        return interact(response)
    else:
        return acknowledge()
