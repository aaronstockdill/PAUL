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


def process(sentence):
    ''' Process the sentence, and go to wolfram Alpha '''
    sentence.replace_it()
    
    query = "+".join([word[0] for word in sentence.sentence_string])
    os.system("open http://www.wolframalpha.com/input/?i=" 
               + quote(query).replace("%2B", "+"))

def main():
    ''' The main function '''
    
    words = {word: ("discover", "noun") for word in NOUNS}
    
    user_info.associate(words)
    user_info.word_actions["wikipedia"] = lambda sentence: process(sentence)
    
    user_info.log("Successfully imported " + __name__)

main()