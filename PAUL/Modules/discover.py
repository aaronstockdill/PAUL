"""
discover.py
If all else fails, try Google. 
Author: Aaron Stockdill
"""

import os

import paul
from urllib.parse import quote

NOUNS = [
    "lucky",
]

VERBS = [
    "discover",
    "search",
]

def is_math(sentence):
    ''' Determines if any part of the sentence is math '''
    for word, _ in sentence:
        if paul.has_one_of(word, "+/^*-=") and not word.startswith("http"):
            return True
    return False


def process(sentence):
    ''' Process the sentence, and go to Google '''
    
    if is_math(sentence):
        return sentence.forward("math")
    
    sentence.replace_it()
    
    engines = {
        "google": "http://www.google.com/search?q={}",
        "bing": "http://www.bing.com/search?q={}",
        "yahoo": "http://search.yahoo.com/search?p={}",
        "duckduckgo": "https://duckduckgo.com/?q={}",
        "baidu": "http://www.baidu.com/s?wd={}",
    }
    engine = paul.get_search_engine().lower()
    
    keywords = sentence.keywords(ignore=[engine])
    paul.log("KEYWORDS:", keywords)
    
    query = "+".join([word.replace(" ", "+") for word, _ in keywords
                      if word not in VERBS+NOUNS])
    url = (engines[engine].format(query))
    
    paul.log("URL: " + url)
    paul.loading()
    paul.open_URL(url)
    return "Here, try this."

def main():
    ''' The main function '''
    VERBS.append(paul.get_search_engine().lower())
    words = {word: ("discover", "noun") for word in NOUNS}
    words.update({word: ("discover", "verb") for word in VERBS})
    
    paul.associate(words)
    paul.register("discover", process)

main()