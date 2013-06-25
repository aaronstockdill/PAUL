"""
weather.py
Lets Paul get the weather from the Yahoo Weather API. 
Author: Aaron Stockdill
"""

import urllib.request
import datetime

import user_info
import brain2

def process(sentence):
    ''' Process the sentence, act as necessary '''
    brain2.loading()
    ignore = ['weather', 'forecast']
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
        day_index = 1
    elif keywords[0][0] in weekdays:
        day_index = weekdays.index(keywords[0][0]) - today + 1
    
    if user_info.VERBOSE: print("DAY:", day_index)
    
    return weather(day_index)

def weather(day_index=0):
    ''' Simply get the weather for today '''
    
    page = urllib.request.urlopen("http://weather.yahooapis.com/"
           "forecastrss?u=c&w=" + user_info.info['woeid'])
    lines = page.readlines()
    lines = [str(line, encoding='utf8') for line in lines[28:48]
             if str(line, encoding='utf8').startswith("<yweather")]
    if user_info.VERBOSE: print("WEATHER_RAW:", lines)
    
    if day_index == 0:
        items = lines[day_index].split("\"")[1:-1]
        items = ['text'] + [item.strip().strip('=') for item in items]
    
        if user_info.VERBOSE: print(items)
    
        condition = items[1].lower()
        temp = int(items[5])
        user_info.info['it'] = "{}°C".format(temp)
        
        return "It's {}°C, and {}.".format(temp, condition)
    
    else:
        items = lines[day_index].split("\"")[1:-1]
        items = ['text'] + [item.strip().strip('=') for item in items]
    
        if user_info.VERBOSE: print("ITEMS:", items)
    
        condition = items[9].lower()
        temp = "{} to {}".format(items[5], items[7])
        user_info.info['it'] = "http://weather.yahoo.com/"
    
        return ("It will have a low of "
               "{}°C, a high of {}°C, and will be {}.".format(
               items[5], items[7], items[9].lower()))

def main():
    ''' The main function '''
    
    known_nouns = {
        "weather": lambda sentence: process(sentence),
        "forecast": lambda sentence: process(sentence),
        "rainy": lambda sentence: process(sentence), 
        "rain": lambda sentence: process(sentence),
        "raining": lambda sentence: process(sentence), 
        "sun": lambda sentence: process(sentence),
        "sunny": lambda sentence: process(sentence), 
        "temperature": lambda sentence: process(sentence),
        "cold": lambda sentence: process(sentence),
        "hot": lambda sentence: process(sentence),
        "humid": lambda sentence: process(sentence),
    }
    
    user_info.nouns_association.update(known_nouns)
    
    if user_info.VERBOSE: print("Successfully imported", __name__)

main()