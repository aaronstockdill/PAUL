"""
weather.py
Lets Paul get the weather from the Yahoo Weather API. 
Author: Aaron Stockdill
"""

import urllib.request
import datetime

import user_info
import brain2

NOUNS = [
    "weather",
    "forecast",
    "rainy",
    "rain",
    "raining",
    "sun",
    "sunny",
    "temperature",
    "cold",
    "hot",
    "humid",
    "today",
    "tomorrow",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"
]

def process(sentence):
    ''' Process the sentence, act as necessary '''
    brain2.loading()
    ignore = [
        "weather",
        "forecast",
        "rainy",
        "rain",
        "raining",
        "sun",
        "sunny",
        "temperature",
        "cold",
        "hot",
        "humid",
    ]
    keywords = sentence.keywords(ignore)
    keywords = [word for word in keywords if word[0] != 'weather']
    if user_info.VERBOSE: print("KEYWORDS:", keywords)
    today = datetime.date.today().weekday()
    if user_info.VERBOSE: print("TODAY:", today)
    
    day_index = 0
    
    weekdays = ['monday', 'tuesday', 'wednesday', 
                'thursday', 'friday', 'saturday', 'sunday']
    
    if len(keywords) == 0 or keywords[0][0] in ['today', 'now', "today's"]:
        day_index = 0
    elif keywords[0][0] in ['tomorrow', "tomorrow's"]:
        day_index = 2
    elif keywords[0][0] in weekdays:
        day_index = weekdays.index(keywords[0][0]) - today + 1
    
    if user_info.VERBOSE: print("DAY:", day_index)
    
    return weather(day_index)

def weather(day_index=0):
    ''' Simply get the weather for today '''
    try:
        page = urllib.request.urlopen("http://weather.yahooapis.com/"
               "forecastrss?u=c&w=" + user_info.info['woeid'])
    except urllib.error.URLError:
        return "I couldn't retrieve the weather."
    lines = page.readlines()
    lines = [str(line, encoding='utf8') for line in lines[28:48]
             if str(line, encoding='utf8').startswith("<yweather")]
    if user_info.VERBOSE: print("WEATHER_RAW:", lines)
    
    user_info.info['it'] = "http://weather.yahoo.com/"
    
    if day_index == 0:
        items = lines[day_index].split("\"")[1:-1]
        items = ['text'] + [item.strip().strip('=') for item in items]
    
        if user_info.VERBOSE: print(items)
    
        condition = items[1].lower()
        temp = int(items[5])
        
        return "It's {}°C, and {}.".format(temp, condition)
    
    else:
        items = lines[day_index].split("\"")[1:-1]
        items = ['day'] + [item.strip().strip('=') for item in items]
    
        if user_info.VERBOSE: print("ITEMS:", items)
    
        condition = items[9].lower()
        temp = "{} to {}".format(items[5], items[7])
    
        return ("It will have a low of "
               "{}°C, a high of {}°C, and will be {}.".format(
               items[5], items[7], items[9].lower()))

def main():
    ''' The main function '''
    
#    known_nouns = {
#        "weather": lambda sentence: process(sentence),
#        "forecast": lambda sentence: process(sentence),
#        "rainy": lambda sentence: process(sentence), 
#        "rain": lambda sentence: process(sentence),
#        "raining": lambda sentence: process(sentence), 
#        "sun": lambda sentence: process(sentence),
#        "sunny": lambda sentence: process(sentence), 
#        "temperature": lambda sentence: process(sentence),
#        "cold": lambda sentence: process(sentence),
#        "hot": lambda sentence: process(sentence),
#        "humid": lambda sentence: process(sentence),
#    }
    
#    words = {
#        "weather": ("weather", "noun"),
#        "forecast": ("weather", "noun"),
#        "rainy": ("weather", "noun"),
#        "rain": ("weather", "noun"),
#        "raining": ("weather", "noun"),
#        "sun": ("weather", "noun"),
#        "sunny": ("weather", "noun"),
#        "temperature": ("weather", "noun"),
#        "cold": ("weather", "noun"),
#        "hot": ("weather", "noun"),
#        "humid": ("weather", "noun"),
#    }
    
    words = {word: ("weather", "noun") for word in NOUNS}
    
    #user_info.nouns_association.update(known_nouns)
    #user_info.word_associations.update(words)
    user_info.associate(words)
    user_info.word_actions["weather"] = lambda sentence: process(sentence)
    
    if user_info.VERBOSE: print("Successfully imported", __name__)

main()