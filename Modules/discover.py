"""
discover.py
If all else fails, try Wolfram Alpha. 
Author: Aaron Stockdill
"""

import os
import user_info
from urllib.parse import quote

def process(sentence):
    ''' Process the sentence, and go to wolfram Alpha '''
    query = "+".join([word[0] for word in sentence])
    os.system("open http://www.wolframalpha.com/input/?i=" 
               + quote(query).replace("%2B", "+"))

def main():
    ''' The main function '''
    if user_info.VERBOSE: print("Successfully imported", __name__)

main()