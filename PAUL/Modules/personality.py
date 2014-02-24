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
    "gidday",
    "g'day",
]

THANKS = [
    "thanks",
    "thank-you",
    "thank",
    "gratitude",
    "thx",
]

FEELING = [
    "feel",
    "feeling",
]

RANDOM = [
    "asdf",
    "1234",
    "joke",
    "sing",
    "song",
] 

class Point(object):
    """ A pointer class, so all variations of a word
        point to the base word """

    def __init__(self, name, dict):
        self.name = name
        self.dict = dict

    def value(self):
        return self.dict[self.name]


def about_me():
    ''' Tell the user about Paul '''
    responses = [
        "I am but a humble assistant{}, doing what I can to serve.",
        "I am simply the finest Digital Assistant that ever was{}.",
        "Well, I'm a bit of 0, a bit of 1, and a bit more{}.",
    ]
    return paul.random_choice(responses)


def random(sentence):
    ''' Reply to something a bit random. '''
    key_words = {
        "asdf": ["jkl;", 
                 "ghjk", 
                 "fdsa", 
                 "No, it's pronounced \"Paul\"!"],
        "1234": ["♪Tell me that you love me more.♪", 
                 "I declaire a thumb war!", 
                 "5, 6, 7, 8.",
                 "5, 6, 9, 10."],
        "joke": ["Knock Knock... Oh blast, I forgot how it goes.",
                 ("Why did the virtual assistant think he was funny?\n\n"
                  + "I'm not sure either."),
                 "Yo' mama. I'm sorry, that was mean."],
        "sing": [("Twinkle Twinkle, virtual assistant,\n" 
                 + "How I wonder, if you existed."),
                 "Sorry, my 'tune' module was never installed.",
                 ("I would, but humans tend to like it when their "
                  + "ears DON'T bleed."),],
    }
    key_words["jokes"] = key_words["joke"]
    key_words["song"] = key_words["sing"]
    for word, _ in sentence:
        if word in key_words.keys():
            return paul.random_choice(key_words[word])


def greet():
    responses = ["Hi{}.", 
                 "Hello{}."]
    d = datetime.datetime.now()
    if d.hour in range(0, 12):
        responses += ["Good Morning{}."]
    elif d.hour in range(12, 18):
        responses += ["Good Afternoon{}."]
    elif d.hour in range(18, 23):
        responses += ["Good Evening{}."]
    return paul.random_choice(responses)



def thank():
    responses = [
        "You're most welcome{}.",
        "No worries{}.",
        "You're welcome{}.",
        "Of course{}.",
        "It was nothing{}.",
    ]
    return paul.random_choice(responses)


def feeling():
    responses = [
        "Fine{}!",
        "Fine{}!",
        "Great{}!",
        "Good{}!",
        "Wonderful{}!",
        "Fantastic{}!",
    ]
    pt2 = []
    for response in responses:
        pt2.append(response.format(" thanks{}"))
    return paul.random_choice(responses+pt2)



def process(sentence):
    ''' Process the input sentence '''
    
    keywords = sentence.keywords(include=["NS", "VB"])
    
    takeback = "I'm still learning!"
    
    if paul.has_one_of(keywords, GREETINGS):
        takeback = greet()
    elif paul.has_one_of(keywords, THANKS):
        takeback = thank()
    elif paul.has_one_of(keywords, FEELING):
        takeback = feeling()
    elif paul.has_one_of(keywords, RANDOM):
        takeback = random(sentence)
    elif paul.has_one_of(keywords, ["name", "call", "called", "named"]):
        return sentence.forward("settings")
    return takeback

def main():
    ''' The main function '''
    
    NOUNS = KEYWORDS + GREETINGS + THANKS + FEELING + RANDOM
    
    words = {word: ("personality", "noun") for word in NOUNS}
    
    paul.associate(words)
    paul.register("personality", process)

main()
