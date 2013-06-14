"""
This is an attempt at rewriting the brain backend.
It is a little... primitive, right now.
"""
import user_info

VOWELS = ['a', 'e', 'i', 'o', 'u']
NEVER_DOUBLE = ['h', 'w', 'x', 'y', 'n'] # n? Not sure, added to fix a one-off
WHISTLE_SINGLE = ['s', 'x', 'z', 'o']
WHISTLE_DOUBLE = ['sh', 'ch']

class Word(object):
    
    def __init__(self, base):
        self.base = base
    
    def __getitem__(self, key):
        ''' Provide a nice way to access values '''
        return self.items[key]
    
    def __setitem__(self, key, value):
        self.items[key] = value
        
    def __str__(self):
        return self.base
    
    def tag(self):
        return self['tag']

class Verb(Word):
    
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
    
    def __init__(self, base):
        self.base = base
        super().__init__(self.base)
        self.items = {
            'base': self.base,
            'tag': 'P',
            'plural': self.base,
            'possess_plural': self.base,
        }

class PronounSubject(Pronoun):
    
    def __init__(self, base):
        self.base = base
        super().__init__(self.base)
        self.items['tag'] = 'PS'
        self.items['plural'] = ('we' if self.base == "i" else 'they')
        self.items['possess_plural'] = ('our' if self.base == 'i' 
                                               else 'their')

class PronounObject(Pronoun):
    
    def __init__(self, base):
        self.base = base
        super().__init__(self.base)
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
    
    def __init__(self, base, open_ended=True):
        self.base = base
        super().__init__(self.base)
        self.items = {
            'base': self.base,
            'tag': "WH",
            'contracted': self.base + "'s",
            'open_ended': open_ended,
        }


class Article(Word):
    
    def __init__(self):
        self.base = 'the'
        super().__init__(self.base)
        self.items = {
            'base': self.base,
            'tag': "AR",
        }

class Preposition(Word):
    
    def __init__(self, base):
        self.base = base
        super().__init__(self.base)
        self.items = {
            'base': self.base,
            'tag': "PP"
        }


class Name(Word):
    def __init__(self, base):
        self.base = base
        self.name = self.base.capitalize()
        super().__init__(self.base)
        self.items = {
            'base': self.base,
            'name': self.base,
            'display_name': self.name,
            'tag': "X"
        }


class Point(object):
    def __init__(self, name):
        self.name = name
    
    def value(self):
        return vocabulary[self.name]


def add_new():
    for noun in user_info.nouns_association.keys():
        vocabulary.update({noun: Noun(noun),})
    create_irregulars()   
    generate_transforms()


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
                    to_add.update({ item: Point(vocabulary[word].base).value(), })
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
    
    
vocabulary = {
    'paul':        Name('paul'),
    
    'be':          Verb("be"),
    'close':       Verb("close"),
    'open':        Verb("open"),
    'play':        Verb("play"),
    'pause':       Verb("pause"),
    'quit':        Verb("quit"),
    'stop':        Verb("stop"),
    'study':       Verb("study"),
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
    
    'a':           Article(),
    'an':          Article(),
    'the':         Article(),
    'this':        Article(),
    'that':        Article(),
    'these':       Article(),
    'those':       Article(),
    
    'who':         Question("who", open_ended=True),
    'why':         Question("why", open_ended=True),
    'how':         Question("how", open_ended=True),
    'when':        Question("when", open_ended=True),
    'what':        Question("what", open_ended=True),
    'where':       Question("where", open_ended=True),
    
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