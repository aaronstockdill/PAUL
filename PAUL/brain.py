"""
brain.py
A rewrite of brain2.py, this is where the sentence is tagged so it can be
used by the modules more easily, and exactly which module is required is
also decided here. It really is the brain.
Author: Aaron Stockdill
"""

import paul
import Modules

def commands(sentence, recommended=None):
    ''' Process a command, based on nouns and verbs in the sentence '''
    
    actions = {}
    weights = {}
    
    for word, _ in sentence:
        if word in paul.vocab.word_associations:
            modules = [mod for mod, _ in paul.vocab.word_associations[word]]
            for module in modules:
                actions[module] = actions.get(module, 0) + 1
    
    if recommended is not None and recommended in paul.vocab.word_associations:
        modules = [mod for mod, _ in paul.vocab.word_associations[recommended]]
        for module in modules:
            actions[module] = actions.get(module, 0) + 5
    
    paul.log("ACTIONS: " + str(actions))
    
    for key, value in actions.items():
        weights[value] = weights.get(value, []) + [key]
    
    paul.log("WEIGHTS: " + str(weights))
    
    if weights != {}:
        best = weights[sorted(weights.keys(), reverse=True)[0]][0]
        paul.log("BEST: " + str(best))
        return paul.vocab.word_actions[best](sentence)
    else:
        return paul.discover.process(sentence)



def process(line):
    ''' Process the given line '''
    
    sentence = paul.Sentence(line)
    
    paul.log("SENTENCE: " + repr(sentence))
    paul.log("KIND: " + sentence.kind)
    
    if sentence.kind == "IMP" or sentence.kind == "INT":
        reply = commands(sentence)
        return paul.interact(reply)
    else:
        return paul.acknowledge()