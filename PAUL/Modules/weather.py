"""
weather.py
Lets Paul get the weather from the Yahoo Weather API. 
Author: Aaron Stockdill
"""

import urllib.request
import datetime

import paul

NOUNS = [
    "weather",   "forecast",   "rainy",    "rain",
    "raining",   "sunny",      "temperature",
    "cold",      "hot",        "humid",    "today",
    "tomorrow",  "monday",     "tuesday",  "wednesday",
    "thursday",  "friday",     "saturday", "sunday",
]

def manual():
    ''' Return some helpful info for the user. '''
    s = """
        Is it raining, sunny, or a bit cold? I can find out for you, for today,
        or any day in the next 5 or so days. I'll let you know the expected
        temperature, and the conditions for the day. If you ask about today,
        I'll also say how hot it is right now.
        """
    return s



def process(sentence):
    ''' Process the sentence, act as necessary '''
    
    paul.loading()
    ignore = [
        "weather",
        "forecast",
        "rainy",
        "rain",
        "raining",
        "sunny",
        "temperature",
        "cold",
        "hot",
        "humid",
    ]
    
    keywords = sentence.keywords()
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
                day_index = (weekdays.index(day) + today) % 7 + 1
            if day_index == 1:
                day_index = 0
    
    paul.log("DAY: " + str(day_index))
    
    return weather(day_index, sentence)



def comment(sentence, temp, condition):
    ''' Make a comment on what the weather will be like. '''
    warm = 25 if paul.get_temp().lower() == "c" else 77
    cold = 0 if paul.get_temp().lower() == "c" else 32
    if sentence.has_one_of(["hot", "warm", "boiling", "roasting"]):
        if int(temp) <  warm:
            return "Meh. "
        elif int(temp) < cold:
            return "Absolutely not hot! "
        elif int(temp) > warm:
            return "It will be warm. "
    elif sentence.has_one_of(["cold", "cool", "freezing"]):
        if int(temp) > warm:
            return "Definitely not cold, it'll be quite hot. "
        elif int(temp) > cold:
            return "Not particularly cold. "
        elif int(temp) < cold:
            return "It'll be cold, so wrap up warm! "
    return ""



def replace_text(condition):
    ''' Set up a more coherant response as to the conditions. Takes a string,
        returns a string. '''
    
    words = condition.split()
    if words[0].lower() == "am":
        words = words[1:] + ["in", "the", "morning"]
    elif words[0].lower() == "pm":
        words = words[1:] + ["in", "the", "afternoon"]
    return " ".join(words)
    



def get_conditions(raw_data, day_index):
    ''' Return a nice dictionary of the information in raw_data '''
    
    lines = [str(line, encoding='utf8') for line in raw_data[28:48]
             if str(line, encoding='utf8').startswith("<yweather")]
    items = lines[day_index].split("\"")[1:-1]
    pre = ['text'] if day_index == 0 else ['day']
    items = pre + [item.strip().strip('=') for item in items]
    conditions = {}
    for i in range(0, len(items), 2):
        conditions[items[i]] = items[i+1]
    conditions['text'] = replace_text(conditions['text'])
    return conditions



def weather(day_index, sentence):
    ''' Simply get the weather for any day '''
    if day_index > 5 or day_index < 0:
        return "I can't see that far ahead. Sorry!"
    
    try:
        page = urllib.request.urlopen("http://weather.yahooapis.com/"
               "forecastrss?u=" + paul.get_temp().lower() + "&w="
               + paul.get_woeid())
    except urllib.error.URLError:
        return ("I couldn't retrieve the weather. " + 
                "Are you connected to the internet?")
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
        
        com = comment(sentence, temp, conditions['text'])
        return "{0}It's {1}°{2}{3}. The high today is {4}°{2}, {5}.".format(
        com, temp, paul.get_temp(), condition, temp2, condition2)
    
    else:
        condition = conditions['text'].lower()
        com = comment(sentence, conditions['high'], conditions['text'])
        rep = ("{0}It will have a low of "
               "{1}°{2}, a high of {3}°{2}, and will be {4}.".format(
               com, conditions['low'], paul.get_temp(), 
               conditions['high'], condition))
        return rep

def main():
    ''' The main function '''
    
    words = {word: ("weather", "noun") for word in NOUNS}
    
    paul.associate(words)
    paul.register("weather", process)

main()