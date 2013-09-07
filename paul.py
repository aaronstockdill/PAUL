"""
paul.py
Author: Aaron Stockdill

The plan is for this to become the main API for building PAUL modules, rather than importing rather odd things like "brain2" or "user_info" for no apparent reason. Hopefully this will take care of that! It will also hopefully make development easier on my part by keeping everything in more logical places. 
"""

import random
import time
import itertools
import os
import operator

import vocab
import user_info


def log(to_log):
    ''' Log some info to log.txt, and print it on the screen if
        VERBOSE is True '''
    
    log_string = str(to_log)
    log_file = open("log.txt", 'a')
    time_str = time.strftime("%a,%d-%b-%Y~%H:%M ")
    log_file.write(time_str + log_string + "\n")
    log_file.close()
    if user_info.VERBOSE: print(log_string)



def update_words():
    """ Add all the new nouns and verbs from the modules """
    
    for word, values in user_info.word_associations.items():
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



def interact(statement, response=None):
    """ Standard function for interacting with the user. Use this function,
        not anything custom if possible. 'Response' can be 'list', 'y_n', 
        or None """
    
    print(statement)
    if user_info.NOISY: os.system('say "{}"'.format(statement))
    if user_info.SERVER != False:
        log("CONNECTION: " + repr(user_info.SERVER))
        user_info.SERVER.send(bytes(statement + "{}".format(
                                        " " * (1024 - len(statement))),
                                    'utf-8'))
    if response:
        if user_info.SERVER == False:
            bringback = input("> ")
        else:
            user_info.SERVER.send(bytes("paul_done", "utf-8"))
            bringback = user_info.SERVER.recv(1024)
            bringback = str(bringback, encoding="utf8")
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
        ordinal = bringback.get_parts("OR")
        negatives = ['no', 'nope']
        positives = ['yes', 'yep', 'yeah']
    
        if response == 'list':
            if ordinal:
                user_info.log("ORDINALS: " + str(ordinal))
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
    interact(result)
    return result



class Word(object):
    ''' A simple word class that eveything easier to deal with. '''
    
    def __init__(self, word, kind, weight=1):
        ''' Initializer for a word '''
        self.value = word
        self.kind = kind
        self.weight = weight
    
    def __iter__(self):
        return [self.value, self.kind, self.value]
    
    def __repr__(self):
        return "({}, {}, {})".format(self.value, self.kind, self.weight)
    
    def __str__(self):
        return self.value



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
                 in init_string.lower().split(' ')]
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
        

    def keywords(self, ignore=[], include=[]):
        ''' Join things not split by prepositions and stuff, as they probably
            "belong" together. Ideal for getting keywords. If keywords have 
            been found before, use them rather than trying to find them 
            again. This means if the function is called again and again but
            is not stored in a variable, the performance hit is negligible. 
        '''
        
        if self.keyword_list is not None:
            log("KEYWORDS: Short-circuit successful.")
            return self.keyword_list
        else:
            objects = self.get_part("NO", indexes=True)
            names = self.get_part("XO", indexes=True)
            keywords = self.get_part("??", indexes=True)
            
            if include != []:
                other = []
                for key in include:
                    part = self.get_part(key, indexes=True)
                    if part:
                        other = other + part
            else:
                other = None
    
            all_together = []
    
            if objects:
                all_together += objects
            if names:
                all_together += names
            if keywords:
                all_together += keywords
            if other:
                all_together += other
    
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
        
            self.keyword_list = sorted(final_list, 
                                       key=operator.itemgetter(1))
            return self.keyword_list
    
    
    def group_together(self):
        log("WARNING: use of 'group_together' is deprecated."
            " Use 'keywords' instead.")
        return self.keywords()


    def log_unknown(self, word, options):
        ''' Log the unknown words that we come across,
            and what we think it is '''
    
        file = open("Unknown_words.csv", "a")
        file.write("'{}': {}\n".format(word, options))
        file.close


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
                log("IT: " + str(user_info.info['it']))
                self.sentence.pop(i)
                self.sentence.insert(i, (user_info.info["it"], "XO"))
                return True
        return False



update_words()

if __name__ == "__main__":
    import doctest
    doctest.testmod()