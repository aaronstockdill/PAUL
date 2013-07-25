"""
discover.py
If all else fails, try Wolfram Alpha. 
Author: Aaron Stockdill
"""

import os
import user_info
from urllib.parse import quote

NOUNS = [
    "wolfram",
]

VERBS = [
    "discover",
]


def process(sentence):
    ''' Process the sentence, and go to wolfram Alpha '''
    sentence.replace_it()
    
    query = "+".join([word for word in sentence.sentence_string.split(' ')])
    os.system("open http://www.wolframalpha.com/input/?i=" 
               + quote(query).replace("%2B", "+"))
    return "Let me find out for you..."

def main():
    ''' The main function '''
    
    words = {word: ("discover", "noun") for word in NOUNS}
    words.update({word: ("discover", "verb") for word in VERBS})
    
    user_info.associate(words)
    user_info.word_actions["discover"] = lambda sentence: process(sentence)
    
    user_info.log("Successfully imported " + __name__)

main()