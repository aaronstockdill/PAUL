"""
brain.py
A rewrite of brain.py, this is where the sentence is tagged so it can be
used by the modules more easily, and exactly which module is required is
also decided here. It really is the brain.
Author: Aaron Stockdill
"""

import random
import os

import vocab
import user_info
from Modules.importer import *

def interact(statement, response=None):
    """ Standard function for interacting with the user. Use this function,
        not anything custom if possible. Response can be 'list', 'y_n', 
        or None """
        
    if user_info.NOISY: os.system('say "{}"'.format(statement))
    print(statement)
    if response:
        bringback = input("> ")
        words = [clean(word) for word in bringback.lower().split(' ')]
        sentence = tag_sentence(words)
        ordinal = get_parts(sentence, "OR")
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
    


def log_unknown(word, options):
    ''' Log the unknown words that we come across, and what we think it is '''
    
    file = open("Unknown_words.csv", "a")
    file.write("'{}': {}\n".format(word, options))
    file.close


def get_parts(sentence, part, indexes=False, prepositions=False):
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
        parts = [word[0] for word in sentence if word[1] in part]
    else:
        parts = [(word[0], sentence.index(word)) 
                 for word in sentence if word[1] in part]
    if len(parts) > 0:
        return parts
    elif not prepositions:
        return get_parts(sentence, part, prepositions=True)
    else:
        return None


def commands(sentence):
    ''' Process a command, based on nouns and verbs in the sentence '''
    
    subs = get_parts(sentence, "NS")
    objs = get_parts(sentence, "NO")
    if subs and objs:
        objects = subs + objs
    elif subs:
        objects = subs
    elif objs:
        objects = objs
    else:
        objects = None
    
    verbs = get_parts(sentence, "VB")
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
                user_info.verbs_association[verb](sentence)
    elif verb in user_info.verbs_association:
        object_noun = "it"
        return user_info.verbs_association[verb](sentence)
    discover.process(sentence)
    return "Let me find out for you..."


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


def clean(word):
    ''' Clean the text, removing unwanted characters '''
    
    for to_remove in list(" ,.?'\";:\\!$&<>@#%^*{}[]+-=_"):
        word = word.strip(to_remove)
    return word


def tag_word(word):
    """ Tag the word's part of speech, returning the word's base and tag
        in a tuple """
    
    if word not in vocab.vocabulary:
        return (word, "??")
    else:
        return (vocab.vocabulary[word].base, vocab.vocabulary[word].tag())

def guess_unknown(sentence):
    ''' See if it can work out what the ?? is '''
    
    vital_parts = ["NS", "NO", "VB"]
    for word in sentence:
        if word[1] in ["NS", "PS", "WH"]:
            if "NS" in vital_parts:
                vital_parts.remove("NS")
        elif word[1] in ["NO", "PO"]:
            if "NO" in vital_parts:
                vital_parts.remove("NO")
        elif word[1] == "VB":
            if "VB" in vital_parts:
                vital_parts.remove("VB")
    
    for word in sentence:
        if word[1] == "??":
            log_unknown(word[0], vital_parts)
            if len(vital_parts) == 1:# and vital_parts[0] == "NO":
                i = sentence.index(word)
                sentence.pop(i)
                sentence.insert(i, (word[0], vital_parts[0]))
                if user_info.VERBOSE: print("UNKNOWN WORD:", word)
    
    return sentence

def classify(sentence):
    ''' Determines what the concept of the sentence is.
        Can be declarative (DEC), Interrogative (INT),
        or Imperative (IMP)'''
        
    if (sentence[0][1] == "VB" or 
        sentence[0][0] == user_info.info["computer"]):
        kind = "IMP"
        sentence.insert(0, ("You", "PS"))
    elif sentence[0][1] == "WH":
        kind = "INT"
    else:
        kind = "DEC"
    return kind


def tag_sentence(words):
    ''' Tag all the words in a sentence, applying various rules as
        necessary to fix up oddities '''
    
    sentence = []
    verb_index = 999999
    object_index = 999999
    for i in range(len(words)):
        word = words[i]
        base, part = tag_word(word)
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
        

def process(line):
    ''' Process the given line '''
    
    words = [clean(word) for word in line.lower().split(' ')]
    sentence = tag_sentence(words)
    
    sentence = guess_unknown(sentence)
    if user_info.VERBOSE: print("SENTENCE:", sentence)
    sentence_kind = classify(sentence)
    if user_info.VERBOSE: print("KIND:", sentence_kind)
    
    if sentence_kind == "IMP" or sentence_kind == "INT":
        response = commands(sentence)    
        return interact(response)
    else:
        return acknowledge()
