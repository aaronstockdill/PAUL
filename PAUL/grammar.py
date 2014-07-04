'''
S = Sentence
N = Noun
V = Verb
P = Preposition
W = Question
A = Adjective
B = Adverb


S -> N V N | N V | V | W V N
N -> A N | P N | P | noun
V -> B V | V B | verb
P -> preposition
W -> question
A -> A A | adjective
B -> B B | adverb
'''

class Scanner(object):
    def __init__(self, sentence):
        self.sentence = sentence
        self.pos = 0
    
    def consume(self):
        w = self.lookahead()
        self.pos += 1
        return w
    
    def lookahead(self, dist=0):
        if self.pos+dist < len(self.sentence):
            return self.sentence[self.pos+dist]
        else:
            return None, None

class Sentence(object):
    def __init__(self, *args):
        self.sentence = args
    def __repr__(self):
        return str(self.sentence)
        
class NounPart(object):
    def __init__(self, *arg):
        self.noun_part = arg
    def __repr__(self):
        return str(self.noun_part)

class VerbPart(object):
    def __init__(self, *arg):
        self.verb_part = arg
    def __repr__(self):
        return str(self.verb_part)

class QuestionPart(object):
    def __init__(self, *arg):
        self.question_part = arg
    def __repr__(self):
        return str(self.question_part)

class PronounPart(object):
    def __init__(self, *arg):
        self.pronoun_part = arg
    def __repr__(self):
        return str(self.pronoun_part)

class AdjectivePart(object):
    def __init__(self, *arg):
        self.adjective_part = arg
    def __repr__(self):
        return str(self.adjective_part)

class AdverbPart(object):
    def __init__(self, *arg):
        self.adverb_part = arg
    def __repr__(self):
        return str(self.adverb_part)




def sentence():
    if scanner.lookahead()[1] == 'WH':
        w = question()
        n1 = noun()
        v = verb()
        n2 = noun()
        return Sentence(w, n1, v, n2)
    elif scanner.lookahead()[1] == "VB":
        return Sentence(verb())
    elif scanner.lookahead()[1] == "NS":
        n1 = noun()
        v = verb()
        if scanner.lookahead()[1][0] in ["N", "P"]:
            return Sentence(n1, v, noun())
        else:
            return Sentence(n1, v)
    else:
        n1 = noun()
        v = verb()
        if scanner.lookahead()[1] and scanner.lookahead()[1][0] in ["N", "P"]:
            return Sentence(n1, v, noun())
        else:
            return Sentence(n1, v)

def question():
    return QuestionPart(scanner.consume())

def pronoun():
    return PronounPart(scanner.consume())
    
def noun():
    if scanner.lookahead()[1][0] == "N":
        return NounPart(scanner.consume())
    elif scanner.lookahead()[1][0] == "P":
        p = pronoun()
        if scanner.lookahead()[1] and scanner.lookahead()[1][0] == "N":
            n = noun()
            return NounPart(p, n)
        else:
            return NounPart(p)
    elif scanner.lookahead()[1] == "AD":
        a = adjective()
        n = noun()
        return NounPart(a, n)
    else:
        return NounPart(scanner.consume())

def verb():
    if scanner.lookahead()[1] == "AV":
        a = adverb()
        v = verb()
        return VerbPart(a, v)
    else:
        return VerbPart(scanner.consume())

def adjective():
    a = scanner.consume()
    if scanner.lookahead()[1] == 'AD':
        return AdjectivePart(a, scanner.consume())
    else:
        return AdjectivePart(a)

scanner = Scanner([('You', 'PS'), ('tell', 'VB'), ('me', 'PO'), ('about', 'PP'), ('neverland', 'NO')])

print(sentence())