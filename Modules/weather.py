"""
weather.py
Lets Paul get the weather from the Yahoo Weather API. 
Author: Aaron Stockdill
"""

import urllib.request
import user_info
import brain2

def process(sentence):
    ''' Process the sentence, act as necessary '''
    brain2.acknowledge()
    return weather()

def weather():
    ''' Simply get the weather for today '''
    
    page = urllib.request.urlopen("http://weather.yahooapis.com/forecastrss?u=c&w="
        + user_info.info['woeid'])
    lines = page.readlines()
    items = str(lines[28], encoding='utf8').split("\"")[1:-1]
    items = ['text'] + [item.strip().strip('=') for item in items]
    
    condition = items[1].lower()
    
    temp = int(items[5])
    
    user_info.info['it'] = "{}°C".format(temp)
    
    return "It's {}°C, and {}.".format(temp, condition)

def main():
    ''' The main function '''
    
    known_nouns = {
        "weather": lambda sentence: process(sentence), 
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