"""
personality.py
Let Paul get a bit friendlier. 
Author: Aaron Stockdill
"""

import random
import datetime

import paul

KEYWORDS = [
    "personality",
]

GREETINGS = [
    "hi",
    "hello",
    "greetings",
    "salutations",
    "morning",
    "evening",
    "howdy",
    "wassup",
    "sup",
    "yo",
    "ello",
]


def one_of(list):
    name = random.choice(['', ', {}'.format(paul.user_info.info['name'])])
    return random.choice(list).format(name)


def greet():
    name = random.choice(['', ', {}'.format(paul.user_info.info['name'])])
    responses = ["Hi{}.", 
                 "Hello{}."]
    d = datetime.datetime.now()
    if d.hour in range(0, 12):
        responses += ["Good Morning{}."]
    elif d.hour in range(12, 18):
        responses += ["Good Morning{}."]
    elif d.hour in range(18, 23):
        responses += ["Good Evening{}."]
    return one_of(responses)



def process(sentence):
    ''' Process the input sentence '''
    
    keywords = sentence.keywords(include=["NS", "VB"])
    
    takeback = "I'm still learning!"
    
    if paul.has_one_of(keywords, GREETINGS):
        takeback = greet()
    elif paul.has_one_of(keywords, ["name", "called", "named"]):
        return sentence.forward("settings")
    return takeback

def main():
    ''' The main function '''
    
    NOUNS = KEYWORDS + GREETINGS
    
    words = {word: ("personality", "noun") for word in NOUNS}
    #words.update({word: ("personality", "verb") for word in VERBS})
    
    paul.associate(words)
    paul.vocab.word_actions["personality"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()
