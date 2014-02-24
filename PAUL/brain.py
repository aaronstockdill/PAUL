"""
brain.py
A rewrite of brain2.py, this is where the sentence is tagged so it can be
used by the modules more easily, and exactly which module is required is
also decided here. It really is the brain.
Author: Aaron Stockdill
"""

import paul
import importlib
import tutorial

Modules = None

def custom_statements(line):
    ''' Provide access to the user's custom actions, stored in a dict in
        the user's profile. '''
    actions = paul.system.flags["USER"]["actions"]
    if actions != {}:
        for key, value in actions.items():
            actions[key.lower()] = value
        try:
            scpt = actions[line.lower()]
            paul.run_script('automator "{}"'.format(scpt), language="bash")
            return True
        except KeyError:
            return False

def transform_idioms(sentence):
    ''' Take simple idioms, and transform them into a more literal sentence
        for Paul to parse. Takes in a string, returns a string. '''
    idioms = {
        "how are you" : "what are you feeling",
        "how do you do" : "hello",
        "paul": "", # Paul doesn't need to respond to just his name...
        "tell me more": "open it",
    }
    for idiom in idioms.keys():
        if idiom in sentence:
            return sentence.replace(idiom, idioms[idiom])
    return sentence



def load_settings(username):
    ''' Load the settings for the given user. 
        Returns a dictionary of settings. '''
    
    i = importlib.import_module("Settings.{}".format(username))
    info = i.info.copy()
    name = info["name"]
    paul.vocab.vocabulary[name] = paul.vocab.Name(name)
    return info



def login(username):
    ''' Try and log in under the name given '''
    if username == "default" or username == "guest":
        paul.system.flags["USER"] = load_settings("default")
        return True
    elif username == "new user":
        import new_user
        name = paul.interact("Absolutely! What is your name? ",
                             response="arb")
        new_user.main(name)
        paul.system.flags["USER"] = load_settings(name.lower())
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
    paul.system.flags["SEND"] = output_fun
    paul.system.flags["GET"] = input_fun
    paul.system.flags["EXEC"] = exec_fun
    


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
    global Modules
    if not Modules:
        import Modules
    
    custom = custom_statements(line)
    if custom:
        return None
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
