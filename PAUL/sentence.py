"""
sentence.py
Author: Aaron Stockdill

Breaking sentence into its own file. Hopefully this will keep things a little 
more organised.
"""

import vocab
import itertools
import operator

def join_lists(*lists):
    ''' Joins the lists. Arguments are lists that get joined, but are
        quitely ignored if not a list. The newly created list is returned. '''

    connected = []
    for item in lists:
        if isinstance(item, list):
            connected += item
    return connected

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
            TypeError: init_string must be a string '''


        if type(init_string) != str:
            raise TypeError("init_string must be a string")

        words = [self.clean(word) for word
                 in init_string.strip().lower().split(' ')]
        self.sentence_string = " ".join(words)
        self.sentence = self.tag_sentence(words)
        self.kind = self.classify()
        self.diagram = self.diagram()


    def __repr__(self):
        ''' Reveal how the sentence is thought of in Python

            >>> Sentence("This is a doctest.")
            [('this', 'PS'), ('be', 'VB'), ('the', 'AR'), ('doctest', '??')] '''
        return str(self.sentence)


    def __str__(self):
        ''' A 'pretty' representation of the sentence.

            >>> print(Sentence("This is a doctest."))
            this is a doctest '''
        return self.sentence_string


    def __iter__(self):
        ''' For iterating over the words in the sentence. '''
        return iter(self.sentence)
    
    
    
    def diagram(self):
        ''' Take the list of (word, type) pieces and return a sentence diagram
            in a tree structure. '''
        
        def nouner(NP):
            N = []
            AR = []
            AD = []
            PP = []
            prepped = False
            for word, part in NP:
                if part == "PP":
                    prepped = True
                if not prepped:
                    if part[0] == "N" or part in ["PS", "PO"]:
                        N.append(word)
                    elif part == "AR":
                        AR.append(word)
                    else:
                        AD.append(word)
                else:
                    PP.append((word, part))
            return [("N", N), ("AR", AR), ("AD", AD), ("PP", prepper(PP))]
            
        def prepper(PP):
            if len(PP) > 1:
                return [("PP", PP[0][0]), nouner(PP[1:])]
            elif len(PP) == 1:
                return [("PP", PP[0][0])]
            else:
                return []
        
        S = []
        NP = []
        VP = []
        verbed = False
        for word, part in self.sentence:
            if part == "VB":
                verbed = True
            if not verbed:
                NP.append((word, part))
            else:
                VP.append((word, part))
        
        NP1 = nouner(NP)
        VP1 = []
        MOD = []
        NO = []
        PP = []
        prepped = False
        for word, part in VP[1:]:
            if word[-2:] == "ly":
                MOD.append(word)
            else:
                NO.append((word, part))
        NP2 = nouner(NO)
        VP1 = [("V", [VP[0][0]]), ("MOD", MOD)]
        if NO:
            VP1.append(("NP", NP2))
        S = [("NP", NP1), ("VP", VP1)]
        return S
    


    def keywords(self, ignore=None, include=None):
        ''' Join things not split by prepositions and stuff, as they probably
            "belong" together. Ignore certain words by putting them in the
            ignore list. Include a certain type of word by listing the types
            in include. By default, keywords gets ?? (unknowns), NO (objects)
            and XO (names). '''

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
            anyway. If there is still nothing, it returns None. '''

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