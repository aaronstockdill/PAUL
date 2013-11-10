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
    
    keywords = sentence.keywords()
    keywords = [word for word in keywords]
    paul.log("KEYWORDS: " + str(keywords))
    
    today = datetime.date.today().weekday()
    paul.log("TODAY: " + str(today))
    
    day_index = 0
    
    weekdays = ['monday', 'tuesday', 'wednesday', 
                'thursday', 'friday', 'saturday', 'sunday']
    
    if (len(keywords) == 0 
        or paul.has_one_of(keywords, ['today', 'now', "today's"])):
        day_index = 0
    elif paul.has_one_of(keywords, ['tomorrow', "tomorrow's"]):
        day_index = 2
    elif paul.has_one_of(keywords, weekdays):
        for day in weekdays:
            if paul.has_word(keywords, day):
                paul.log("DAY:", day)
                day_index = (weekdays.index(day) + today - 4) % 7
            if day_index == 1:
                day_index = 0
    
    paul.log("DAY: " + str(day_index))
    
    return weather(day_index)


def get_conditions(raw_data, day_index):
    ''' Return a nice dictionary of the information in raw_data '''
    
    lines = [str(line, encoding='utf8') for line in raw_data[28:48]
             if str(line, encoding='utf8').startswith("<yweather")]
    items = lines[day_index].split("\"")[1:-1]
    items = ['text'] + [item.strip().strip('=') for item in items]
    conditions = {}
    for i in range(0, len(items), 2):
        conditions[items[i]] = items[i+1]
    return conditions



def weather(day_index=0):
    ''' Simply get the weather for any day '''
    if day_index > 5 or day_index < 0:
        return "I can't see that far ahead. Sorry!"
    
    try:
        page = urllib.request.urlopen("http://weather.yahooapis.com/"
               "forecastrss?u=" + paul.user_info.info['temp'].lower() + "&w="
               + paul.user_info.info['woeid'])
    except urllib.error.URLError:
        return "I couldn't retrieve the weather. Are you connected to the internet?"
    lines = page.readlines()    
    conditions = get_conditions(lines, day_index)
    
    paul.log("WEATHER_RAW:", lines)
    paul.log("CONDITIONS:", conditions)
    
    paul.set_it("http://weather.yahoo.com/")
    
    if day_index == 0:
        condition = (", and {}".format(conditions['text'].lower()) 
                     if conditions['text'].lower() != "unknown" else "")
        temp = conditions['temp']
        
        conditions2 = get_conditions(lines, 1)
        paul.log("CONDITIONS2:", conditions2)
    
        condition2 = conditions2['text'].lower()
        temp2 = "{}".format(conditions2['high'])
        
        return "It's {0}°{1}{2}. The high today is {3}°{1}, {4}.".format(
        temp, paul.user_info.info['temp'], condition, temp2, condition2)
    
    else:
        condition = conditions['text'].lower()
    
        rep = ("It will have a low of "
               "{0}°{1}, a high of {2}°{1}, and will be {3}.".format(
               conditions['low'], paul.user_info.info['temp'], 
               conditions['high'], condition))
        return rep

def main():
    ''' The main function '''
    
    words = {word: ("weather", "noun") for word in NOUNS}
    
    paul.associate(words)
    paul.vocab.word_actions["weather"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()