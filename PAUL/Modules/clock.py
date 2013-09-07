'''
clock.py
A clock program to deal with simple requests in regards to times, etc.
Author: Aaron Stockdill
'''

import time
import paul

NOUNS = [
    "time",
    "date",
    "hour",
    "minute",
    "day",
    "date",
    "month",
    "year",
]

DAYS =[
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

MONTHS = [
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'july',
    'august',
    'september',
    'october',
    'november',
    'december',
]

def process(sentence):
    ''' Process the sentence '''
    
    keywords = sentence.keywords(include=["NS"])
    keywords = [word[0] for word in keywords]
    new_keys = []
    for keyword in keywords:
        for word in keyword.split():
            new_keys.append(word)
    keywords = new_keys
    paul.log("KEYWORDS: " + str(keywords))
    
    time_str = time.strftime("%I:%M%p").lower()
    time_str = time_str[1:] if time_str.startswith("0") else time_str
    
    return what_keyword(keywords[0])


def what_keyword(keyword=time):
    ''' Return what __ it is, e.g. time, day, etc. '''
    if keyword == "time":
        time_str = time.strftime("%I:%M%p").lower()
        answer = time_str[1:] if time_str.startswith("0") else time_str
    elif keyword == "day" or keyword in DAYS:
        answer = time.strftime("%A")
    elif keyword == "month" or keyword in MONTHS:
        answer = time.strftime("%B")
    elif keyword == "year":
        answer = time.strftime("%Y")
    elif keyword == "date":
        answer = time.strftime("%A, %d %B %Y")
    
    return "It is {}.".format(answer)

### TODO: "what will the date be next tuesday?"

def main():
    ''' The main function '''
    words = {word: ("clock", "noun") for word in NOUNS}
    words.update({word: ("clock", "noun") for word in DAYS})
    words.update({word: ("clock", "noun") for word in MONTHS})
    
    paul.associate(words)
    paul.vocab.word_actions["clock"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()