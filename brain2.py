"""
A rewrite of brain.
"""

import random
import os

import vocab
import user_info
from Modules.importer import *

def interact(statement, response=False):
    if user_info.NOISY: os.system('say "{}"'.format(statement))
    print(statement)
    if response:
        bringback = input("> ")
        words = [clean(word) for word in bringback.lower().split(' ')]
        sentence = tag_sentence(words)
        ordinal = get_parts(sentence, "OR")
        declines = ['none', 'neither']
        if ordinal:
            if user_info.VERBOSE: print("ORDINALS: ", ordinal)
            return vocab.vocabulary[ordinal[0]]['value']
        elif bringback.lower() in declines:
            return None
        if user_info.VERBOSE: print("NUMBER:", int(bringback))
        return int(bringback)
    


def log_unknown(word, options):
    file = open("Unknown_words.csv", "a")
    file.write("'{}': {}\n".format(word, options))
    file.close


def get_parts(sentence, part, indexes=False, prepositions=False):
    ''' return the first object in a sentence, or None '''
    if part == "NO" or part == "XO":
        if prepositions:
            part = ["NO", "PO"]
        else:
            part = [part]
    elif part == "NS" or part == "XS":
        if prepositions:
            part = ["NS", "PS"]
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
    ''' process a command '''
    subs = get_parts(sentence, "NS")
    objs = get_parts(sentence, "NO")
    if subs and objs:
        object = subs + objs
    elif subs:
        object = subs
    elif objs:
        object = objs
    else:
        object = None
    
    verb = get_parts(sentence, "VB")[0]
    
    if object is not None:
        object_noun = "the {}".format(object[0])
        if object[0] in user_info.nouns_association:
            return user_info.nouns_association[object[0]](sentence)
        else:
            if verb in user_info.verbs_association:
                user_info.verbs_association[verb](sentence)
    elif verb in user_info.verbs_association:
        object_noun = "it"
        return user_info.verbs_association[verb](sentence)
    discover.process(sentence)
    return "Let me find out for you..."


def acknowledge(sentence):
    name = random.choice(['', ', {}'.format(user_info.info['name'])])
    acknowledgements = [
        "Ok{}.".format(name),
        "Sure{}.".format(name),
        "Whatever you say{}.".format(name),
        "Certainly{}.".format(name),
    ]
    return random.choice(acknowledgements)


def clean(word):
    ''' Clean the text, removing unwanted characters '''
    for to_remove in list(" ,.?'\";:\\!$&<>@#%^*{}[]+-=_"):
        word = word.strip(to_remove)
    return word


def tag(word):
    """ Tag the word's part of speech """
    
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
            if len(vital_parts) == 1 and vital_parts[0] == "NO":
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
    sentence = []
    verb_index = 999999
    object_index = 999999
    for i in range(len(words)):
        word = words[i]
        base, part = tag(word)
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
    else:
        response = acknowledge(sentence)
    
    interact(response)
