"""
brain.py
A rewrite of brain2.py, this is where the sentence is tagged so it can be
used by the modules more easily, and exactly which module is required is
also decided here. It really is the brain.
Author: Aaron Stockdill
"""

import paul
import Modules

def transform_idioms(sentence):
    ''' Take simple idioms, and transform them into a more literal sentence
        for Paul to parse. Takes in a string, returns a string. '''
    idioms = {
        "how are you" : "what are you feeling",
        "how do you do" : "hello",
    }
    for idiom in idioms.keys():
        if idiom in sentence:
            return idioms[idiom]
    return sentence



def load_settings(username):
    ''' Load the settings for the given user. 
        Returns a dictionary of settings. '''
    
    f = open("PAUL/Settings/{}.py".format(username))
    lines = f.readlines()
    f.close()
    
    lines = [line.strip("\n").strip() for line in lines 
             if not (line.startswith("#") 
                     or line.startswith("info = {")
                     or line.startswith("}")
                     or line.strip() == "")]
    info = {}
    for line in lines:
        key, value = line.split(":")
        key = key.strip().strip("\"")
        value = value.strip().strip(",").strip("\"")
        info[key] = value
    
    return info



def login(username):
    ''' Try and log in under the name given '''
    if username == "default":
        paul.system.flags["USER"] = load_settings("default")
        return True
    else:
        if username.lower() in paul.system.users:
            paul.system.flags["USER"] = load_settings(username.lower())
            return True
        else:
            paul.system.flags["USER"] = load_settings("default")
            return False



def set_IO(output_fun, input_fun, exec_fun=None):
    ''' Provide a way to set up interactions with Paul when not using the
        command line. Requires an input function and an output function.
        Optionally needs an execute function, if execution is not to be on
        the same computer as Paul (e.g. networked clients). '''
    paul.user_info.flags["SEND"] = output_fun
    paul.user_info.flags["GET"] = input_fun
    paul.user_info.flags["EXEC"] = exec_fun
    


def commands(sentence):
    ''' Process a command, based on nouns and verbs in the sentence '''

    actions = {}
    weights = {}

    for word, _ in sentence:
        if word in paul.vocab.word_associations:
            modules = [mod for mod, _ in paul.vocab.word_associations[word]]
            for module in modules:
                actions[module] = actions.get(module, 0) + 1/(len(modules))

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
    
    splitters = [" and ", " then ", ", "]
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
    parts = [transform_idioms(i.strip()) for i in parts if i.strip() != ""]
    paul.log("PARTS:", parts)
    
    for part in parts:
        if part != "":
            sentence = paul.Sentence(part)

            paul.log("SENTENCE: " + repr(sentence))
            paul.log("KIND: " + sentence.kind)

            reply = commands(sentence)
            if reply != "" and reply != None:
                paul.interact(reply)
