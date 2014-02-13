"""
vocab.py
This is where the words, their classes, and how to deal with them are all
stored for Paul to deal with.
Author: Aaron Stockdill
"""

VOWELS = ['a', 'e', 'i', 'o', 'u']
NEVER_DOUBLE = ['h', 'w', 'x', 'y', 'n'] # n? Not sure, added to fix a one-off, maybe
WHISTLE_SINGLE = ['s', 'x', 'z', 'o']
WHISTLE_DOUBLE = ['sh', 'ch']

word_associations = {}
word_actions = {}

class Word(object):
    """ A Standard word, providing most of the 'set and get' methods """

    def __init__(self, base):
        self.base = base

    def __getitem__(self, key):
        ''' Provide a nice way to access values '''
        return self.items[key]

    def __setitem__(self, key, value):
        ''' Provide a nice way to set wrong values correctly '''
        self.items[key] = value

    def __str__(self):
        ''' For nice printing should it be necessary '''
        return self.base

    def __len__(self):
        ''' Get the length of a word, for pylint '''
        return len(self.base)

    def __delitem__(self, key):
        ''' Delete one of the wrong items completely '''
        del self.items[key]

    def tag(self):
        ''' A nicer way to get the word tag '''
        return self['tag']


class Verb(Word):
    """ Verbs """

    def __init__(self, base):
        super().__init__(base)

        self.not_doubling = (self.base[-1] in NEVER_DOUBLE
                             and self.base[-2] in VOWELS)
        self.doubling = (self.base[-1] not in VOWELS
                         and self.base[-2] in VOWELS)

        self.items = {
            'base': "to " + self.base,
            'fut_perf': 'will ' + self.base,
            'past_perf': self.__make_past_perf__(),
            'pres_first': self.base,
            'fut_imp': self.__make_fut_imp__(),
            'pres_second': self.base,
            'pres_third': self.__make_pres_imp__(),
            'past_imp': self.__make_past_imp__(),
            'tag': 'VB',
        }

    def __make_past_perf__(self):
        ''' Make the past perfect '''
        past_perf = ''
        if self.base[-1] == 'e':
            past_perf =  self.base[:-1] + 'ed'

        elif (self.base[-1] == 'y'
              and self.base[-2] not in VOWELS):
            past_perf = self.base[:-1] + 'ied'

        elif self.not_doubling:
            past_perf = self.base + 'ed'

        elif self.doubling:
            past_perf = self.base + self.base[-1] + "ed"

        else:
            past_perf =  self.base + 'ed'

        return past_perf

    def __make_past_imp__(self):
        ''' Make the past imperfect '''
        return "was " + self.__make_fut_imp__()

    def __make_fut_imp__(self):
        ''' Make the future imperfect '''
        fut_imp = ''

        if self.base[-2:] == 'ie':
            fut_imp =  self.base[:-1] + 'ying'

        elif self.base[-1] == 'e':
            fut_imp =  self.base[:-1] + 'ing'

        elif self.not_doubling:
            fut_imp = self.base + 'ing'

        elif self.doubling:
            fut_imp = self.base + self.base[-1] + "ing"

        else:
            fut_imp = self.base + 'ing'

        return fut_imp

    def __make_pres_imp__(self):
        ''' Generate the present_imperfect '''
        pres_imp = ''

        if (self.base[-1] in WHISTLE_SINGLE
            or self.base[-2:] in WHISTLE_DOUBLE):
            pres_imp = self.base + 'es'

        elif (self.base[-1] == 'y'
              and self.base[-2] not in VOWELS):
            pres_imp = self.base[:-1] + 'ies'

        else:
            pres_imp = self.base + 's'

        return pres_imp

    def perfect(self, bool):
        ''' Return a search terminator based on perfect or not '''
        return "_perf" if bool else "_imp"

    def past(self, perfect=True):
        ''' Access past items nicely '''
        return self["past" + self.perfect(perfect)]

    def present(self, person="first"):
        ''' access present items nicely '''
        if person == "third":
            terminal = "_third"
        elif person == "second":
            terminal = "_second"
        else:
            terminal = "_first"
        return self["pres" + terminal]

    def future(self, perfect=True):
        ''' access future items nicely '''
        return self["fut" + self.perfect(perfect)]



class Noun(Word):
    ''' Nouns '''

    def __init__(self, base, action=None):
        super().__init__(base)

        self.items = {
            'base': self.base,
            'possess': self.__possessive__(),
            'plural': self.__pluralize__(),
            'possess_plural': self.__pos_plur__(),
            'tag': 'N',
            'action': action,
        }

    def __pluralize__(self):
        plural = ''

        if (self.base[-1] in WHISTLE_SINGLE
            or self.base[-2:] in WHISTLE_DOUBLE
            or self.base[-1] == "o"):
            plural = self.base + 'es'

        elif (self.base[-1] == 'y'
              and self.base[-2] not in VOWELS):
            plural = self.base[:-1] + 'ies'

        else:
            plural = self.base + 's'

        return plural

    def __possessive__(self):
        possess = ''

        possess = self.base + "'s"

        return possess

    def __pos_plur__(self):
        return self.__pluralize__() + "'s"

    def plural(self, possessive=False):
        if possessive:
            return self['possess_plural']
        else:
            return self['plural']

    def possessive(self, plural=False):
        if plural:
            return self['possess_plural']
        else:
            return self['possess']


class Pronoun(Word):
    ''' Pronouns '''

    def __init__(self, base):
        super().__init__(base)
        self.items = {
            'base': self.base,
            'tag': 'P',
            'plural': self.base,
            'possess_plural': self.base,
        }

class PronounSubject(Pronoun):
    ''' Subject Pronouns '''

    def __init__(self, base):
        super().__init__(base)
        self.items['tag'] = 'PS'
        self.items['plural'] = ('we' if self.base == "i" else 'they')
        self.items['possess_plural'] = ('our' if self.base == 'i'
                                               else 'their')

class PronounObject(Pronoun):
    ''' Object Pronouns '''

    def __init__(self, base):
        super().__init__(base)
        self.bases = {
            'me': 'i',
            'him': 'he',
            'her': 'she'
        }
        self.items['tag'] = 'PO'
        self.items['plural'] = ('us' if self.base == "we" else 'them')
        self.items['base'] = self.bases[self.base]
        self.items['possess_plural'] = ('ours' if self.base == 'i'
                                               else 'theirs')


class Question(Word):
    ''' Questioning Words '''

    def __init__(self, base, open_ended=True):
        super().__init__(base)
        self.items = {
            'base': self.base,
            'tag': "WH",
            'contracted': self.base + "'s",
            'open_ended': open_ended,
        }


class Article(Word):
    ''' Articles '''

    def __init__(self):
        super().__init__('the')
        self.items = {
            'base': self.base,
            'tag': "AR",
        }

class Preposition(Word):
    ''' Prepositions '''

    def __init__(self, base):
        super().__init__(base)
        self.items = {
            'base': self.base,
            'tag': "PP"
        }


class Name(Word):
    ''' Names '''

    def __init__(self, base):
        super().__init__(base)
        self.name = self.base.capitalize()
        self.items = {
            'base': self.base,
            'name': self.base,
            'display_name': self.name,
            'tag': "X"
        }


class Number(Word):
    ''' Number '''

    def __init__(self, base):
        super().__init__(base)
        self.items = {
            'base': self.base,
            'tag': "NU",
        }



#####  ALL WORD DEFINITIONS DONE  #####


class Point(object):
    """ A pointer class, so all variations of a word
        point to the base word """

    def __init__(self, name):
        self.name = name

    def value(self):
        return vocabulary[self.name]



def generate_transforms():
    ''' Generate all forms of a verb to check for, which point to the root '''

    parts_dict = {}
    to_add = False
    for word in vocabulary.keys():
        to_add = {}
        for key, item in vocabulary[word].items.items():
            if (key != 'base'
            and key != 'tag'
            and key != 'open_ended'
            and key != 'action'):
                to_add.update({
                    item: Point(vocabulary[word].base).value(),
                })
        if to_add:
            parts_dict.update(to_add)
    vocabulary.update(parts_dict)


def create_irregulars():
    ''' Fix the irregular verb 'to be' (Extend as necessary) '''
    vocabulary['be']['past_perf'] = 'had'
    vocabulary['be']['past_imp'] = 'have'
    vocabulary['be']['pres_first'] = 'am'
    vocabulary['be']['pres_second'] = 'are'
    vocabulary['be']['pres_third'] = 'is'
    vocabulary['be']['fut_imp'] = 'am going to be'

    vocabulary['get']['past_perf'] = 'got'

    vocabulary['i']['plural'] = 'we'
    vocabulary['i']['possessive'] = 'my'

    vocabulary['you']['plural'] = 'you'
    vocabulary['you']['possessive'] = 'your'

    vocabulary['he']['possessive'] = 'his'
    vocabulary['him']['possessive'] = 'his'

    vocabulary['she']['possessive'] = 'her'
    vocabulary['her']['possessive'] = 'hers'

    vocabulary['find']['past_perf'] = 'found'

def create_ordinals():
    ords = ['two', 'six', 'four', 'three', 'zero', 'seven', 'nine', 'five', 'one', 'eight', 'seventy', 'sixty', 'twenty', 'ten', 'forty', 'thirty', 'eighty', 'ninety', 'fifty', 'ninth', 'second', 'eighth', 'first', 'third', 'sixth', 'seventh', 'zeroth', 'fourth', 'fifth', 'nineteen', 'twelve', 'seventeen', 'sixteen', 'eleven', 'eighteen', 'fifteen', 'fourteen', 'thirteen', 'twelfth', 'trillion', 'thousand', 'million', 'hundred', 'billion', 'seventieth', 'sixtieth', 'twentieth', 'fortieth', 'thirtieth', 'eightieth', 'ninetieth', 'fiftieth', 'trillionth', 'thousandth', 'millionth', 'hundredth', 'billionth', 'tenth', 'nineteenth', 'seventeenth', 'sixteenth', 'eleventh', 'eighteenth', 'fifteenth', 'fourteenth', 'thirteenth']
    for o in ords:
        vocabulary[o] = Number(o)


vocabulary = {
    'paul':        Name('paul'),

    'be':          Verb("be"),
    'will':        Verb("will"),
    'close':       Verb("close"),
    'open':        Verb("open"),
    'play':        Verb("play"),
    'pause':       Verb("pause"),
    'quit':        Verb("quit"),
    'stop':        Verb("stop"),
    'shut':        Verb("shut"),
    'show':        Verb("show"),
    'get':         Verb("get"),
    'find':        Verb("find"),
    'look':        Verb("look"),
    'call':        Verb("call"),
    'name':        Verb("name"),
    'reveal':      Verb("reveal"),
    'launch':      Verb("launch"),
    'locate':      Verb("locate"),

    'i':           PronounSubject("i"),
    'me':          PronounObject("me"),
    'he':          PronounSubject("he"),
    'him':         PronounObject("him"),
    'she':         PronounSubject("she"),
    'her':         PronounObject("her"),
    'you':         Pronoun("you"),
    'it':          Pronoun("it"),
    'this':        Pronoun("this"),
    'that':        Pronoun("that"),
    'these':       Pronoun("these"),
    'those':       Pronoun("those"),

    'a':           Article(),
    'an':          Article(),
    'the':         Article(),

    'who':         Question("who", open_ended=True),
    'why':         Question("why", open_ended=True),
    'how':         Question("how", open_ended=True),
    'when':        Question("when", open_ended=True),
    'what':        Question("what", open_ended=True),
    'where':       Question("where", open_ended=True),
    'was':         Question("was", open_ended=False),

    'about':       Preposition("about"),
    'above':       Preposition("above"),
    'across':      Preposition("across"),
    'after':       Preposition("after"),
    'against':     Preposition("against"),
    'along':       Preposition("along"),
    'among':       Preposition("among"),
    'around':      Preposition("around"),
    'at':          Preposition("at"),
    'before':      Preposition("before"),
    'behind':      Preposition("behind"),
    'below':       Preposition("below"),
    'beneath':     Preposition("beneath"),
    'beside':      Preposition("beside"),
    'between':     Preposition("between"),
    'beyond':      Preposition("beyond"),
    'but':         Preposition("but"),
    'by':          Preposition("by"),
    'despite':     Preposition("despite"),
    'down':        Preposition("down"),
    'during':      Preposition("during"),
    'except':      Preposition("except"),
    'for':         Preposition("for"),
    'from':        Preposition("from"),
    'in':          Preposition("in"),
    'inside':      Preposition("inside"),
    'into':        Preposition("into"),
    'like':        Preposition("like"),
    'near':        Preposition("near"),
    'of':          Preposition("of"),
    'off':         Preposition("off"),
    'on':          Preposition("on"),
    'onto':        Preposition("onto"),
    'out':         Preposition("out"),
    'outside':     Preposition("outside"),
    'over':        Preposition("over"),
    'past':        Preposition("past"),
    'since':       Preposition("since"),
    'through':     Preposition("through"),
    'throughout':  Preposition("throughout"),
    'till':        Preposition("till"),
    'to':          Preposition("to"),
    'toward':      Preposition("toward"),
    'under':       Preposition("under"),
    'underneath':  Preposition("underneath"),
    'until':       Preposition("until"),
    'up':          Preposition("up"),
    'upon':        Preposition("upon"),
    'with':        Preposition("with"),
    'within':      Preposition("within"),
    'without':     Preposition("without"),
}