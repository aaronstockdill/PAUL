"""
weather.py
Lets Paul get the weather from the Yahoo Weather API. 
Author: Aaron Stockdill
"""

import urllib.request
import datetime

#import user_info
#import brain2

import paul

NOUNS = [
    "weather",   "forecast",   "rainy",    "rain",
    "raining",   "sun",        "sunny",    "temperature",
    "cold",      "hot",        "humid",    "today",
    "tomorrow",  "monday",     "tuesday",  "wednesday",
    "thursday",  "friday",     "saturday", "sunday",
]

def process(sentence):
    ''' Process the sentence, act as necessary '''
    
    paul.loading()
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
    keywords = [word for word in keywords]
    paul.log("KEYWORDS: " + str(keywords))
    
    today = datetime.date.today().weekday()
    paul.log("TODAY: " + str(today))
    
    day_index = 0
    
    weekdays = ['monday', 'tuesday', 'wednesday', 
                'thursday', 'friday', 'saturday', 'sunday']
    
    if len(keywords) == 0 or keywords[0][0] in ['today', 'now', "today's"]:
        day_index = 0
    elif keywords[0][0] in ['tomorrow', "tomorrow's"]:
        day_index = 2
    elif keywords[0][0] in weekdays:
        day_index = weekdays.index(keywords[0][0]) - today + 1
    
    paul.log("DAY: " + str(day_index))
    
    return weather(day_index)



def weather(day_index=0):
    ''' Simply get the weather for today '''
    try:
        page = urllib.request.urlopen("http://weather.yahooapis.com/"
               "forecastrss?u=" + paul.user_info.info['temp'].lower() + "&w="
               + paul.user_info.info['woeid'])
    except urllib.error.URLError:
        return "I couldn't retrieve the weather."
    lines = page.readlines()
    lines = [str(line, encoding='utf8') for line in lines[28:48]
             if str(line, encoding='utf8').startswith("<yweather")]
    
    paul.log("WEATHER_RAW:", str(lines))
    
    paul.user_info.info['it'] = "http://weather.yahoo.com/"
    
    if day_index == 0:
        items = lines[day_index].split("\"")[1:-1]
        items = ['text'] + [item.strip().strip('=') for item in items]
        
        paul.log("ITEMS:", str(items))
    
        condition = items[1].lower()
        temp = int(items[5])
        
        items2 = lines[1].split("\"")[1:-1]
        items2 = ['day'] + [item.strip().strip('=') for item in items2]
        
        paul.log("ITEMS:", str(items2))
    
        condition2 = items2[9].lower()
        temp2 = "{}".format(items2[7])
        
        return "It's {0}°{1}, and {2}. It will get to {3}°{1}, {4}.".format(
        temp, paul.user_info.info['temp'], condition, temp2, condition2)
    
    elif day_index < 0:
        return "I can't see that far ahead. Sorry!"
    
    else:
        items = lines[day_index].split("\"")[1:-1]
        items = ['day'] + [item.strip().strip('=') for item in items]
        
        paul.log("ITEMS: " + str(items))
    
        condition = items[9].lower()
        temp = "{} to {}".format(items[5], items[7])
    
        rep = ("It will have a low of "
               "{}°{}, a high of {}°{}, and will be {}.".format(
               items[5], paul.user_info.info['temp'], items[7],
               paul.user_info.info['temp'], items[9].lower()))
        return rep

def main():
    ''' The main function '''
    
    words = {word: ("weather", "noun") for word in NOUNS}
    
    paul.associate(words)
    paul.vocab.word_actions["weather"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()