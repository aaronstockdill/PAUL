"""
discover.py
If all else fails, try Google's Lucky result. 
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


def process(sentence):
    ''' Process the sentence, and go to wolfram Alpha '''
    sentence.replace_it()
    
    query = "+".join([word for word in sentence.sentence_string.split(' ')
                      if word not in VERBS])
    url = ("http://www.google.com/search?q={}".format(query))
    #url = ("open http://www.google.com/search?q=" 
    #      + quote(query).replace("%2B", "+") + "&btnI")
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