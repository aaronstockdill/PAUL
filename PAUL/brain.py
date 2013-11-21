"""
brain.py
A rewrite of brain2.py, this is where the sentence is tagged so it can be
used by the modules more easily, and exactly which module is required is
also decided here. It really is the brain.
Author: Aaron Stockdill
"""

import paul
import Modules

def commands(sentence):
    ''' Process a command, based on nouns and verbs in the sentence '''

    actions = {}
    weights = {}

    for word, _ in sentence:
        if word in paul.vocab.word_associations:
            modules = [mod for mod, _ in paul.vocab.word_associations[word]]
            for module in modules:
                actions[module] = actions.get(module, 0) + 1/(len(modules))

    paul.log("ACTIONS: " + str(actions))

    for key, value in actions.items():
        weights[value] = weights.get(value, []) + [key]

    paul.log("WEIGHTS: " + str(weights))

    if weights != {}:
        best = weights[sorted(weights.keys(), reverse=True)[0]][0]
        paul.log("BEST: " + str(best))
        return paul.vocab.word_actions[best](sentence)
    else:
        return Modules.discover.process(sentence)


def split_into_parts(line, i=0):
    ''' Break the sentence into the compontent parts, treating each as a new
        command. Allows command chaining. '''
    
    splitters = ["and", "then", ","]
    parts = line.split(splitters[i])
    if len(splitters) == i + 1:
        return parts
    pieces = []
    for part in parts:
        pieces += split_into_parts(part, i+1)
    return pieces



def process(line):
    ''' Process the given line. '''
    
    parts = split_into_parts(line)
    parts = [i.strip() for i in parts if i.strip() != ""]
    paul.log("PARTS:", parts)
    
    for part in parts:
        if part != "":
            sentence = paul.Sentence(part)

            paul.log("SENTENCE: " + repr(sentence))
            paul.log("KIND: " + sentence.kind)

            reply = commands(sentence)
            return paul.interact(reply)
