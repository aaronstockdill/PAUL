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
    "google",
    paul.user_info.info['search_engine'],
]


def process(sentence):
    ''' Process the sentence, and go to Google '''
    sentence.replace_it()
    
    engines = {
        "google": "http://www.google.com/search?q={}",
        "bing": "http://www.bing.com/search?q={}",
        "yahoo": "http://search.yahoo.com/search?p={}",
        "duckduckgo": "https://duckduckgo.com/?q={}",
        "baidu": "http://www.baidu.com/s?wd={}",
    }
    
    keywords = sentence.keywords()
    paul.log("KEYWORDS:", keywords)
    
    query = "+".join([word.replace(" ", "+") for word, _ in keywords
                      if word not in VERBS+NOUNS])
    engine = paul.user_info.info["search_engine"].lower()
    url = (engines[engine].format(query))
    
    paul.log("URL: " + url)
    os.system("open " + url)
    return "Let me find out for you..."

def main():
    ''' The main function '''
    
    words = {word: ("discover", "noun") for word in NOUNS}
    words.update({word: ("discover", "verb") for word in VERBS})
    
    paul.associate(words)
    paul.vocab.word_actions["discover"] = lambda sentence: process(sentence)
    
    paul.log("Successfully imported " + __name__)

main()