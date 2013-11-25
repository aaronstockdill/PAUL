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
    'today',
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
    keywords = paul.filter_unless_listed(keywords, DAYS, MONTHS, NOUNS)
    paul.log("KEYWORDS: " + str(keywords))
    
    return what_keyword(keywords[0])


def what_keyword(keyword="time"):
    ''' Return what <keyword> it is, e.g. time, day, etc. '''
    keyword_map = {
        "time": "%I:%M%p",
        "day": "%A",
        "month": "%B",
        "year": "%Y",
        "date": "%A, %d %B %Y",
    }
    
    if keyword in DAYS:
        keyword = "day"
    elif keyword in MONTHS:
        keyword = "month"
    
    if keyword in keyword_map.keys():
        answer = time.strftime(keyword_map[keyword])
        if keyword == "time":
            answer = answer[1:] if answer.startswith("0") else answer
            answer = answer.lower()
    else:
        time_str = time.strftime("%I:%M%p").lower()
        ans = time_str[1:] if time_str.startswith("0") else time_str
        answer = time.strftime("%A, {}".format(ans))
    paul.set_it(answer)
    return "It is {}.".format(answer)

### TODO: "what will the date be next tuesday?"

def main():
    ''' The main function '''
    words = {word: ("clock", "noun") for word in NOUNS+DAYS+MONTHS}
    
    paul.associate(words)
    paul.register("clock", process)

main()