"""
user_info.py
This is the 'global variable' storage, to share between all the 
different functions. Unfortunately, necessary given the current
designs.
Author: Aaron Stockdill
"""

import time

## Global info that all systems should use. 
info = {
    "woeid": "2348327", # Your WOEID (Yahoo weather location id)
    "name": "Master", # Your Name
    "computer": "paul", # Name of the computer system.
    "it": None, # Whatever 'it' could be, changes automatically, DON'T touch.
    "temp": "C", # Use F for Fahrenheit, C for Celcius.
}

## Flags for the system. Verbose is for debug info, noisy for paul to talk
VERBOSE = True
NOISY = False

## Lists that get updated with what to do with each word
word_associations = {}
word_actions = {}

def associate(words_dict):
    ''' Add this words_dict to the associations list '''
    
    for word, info in words_dict.items():
        old = word_associations.get(word, [])
        word_associations[word] = old + [info]

def log(to_log):
    ''' Log some info to log.txt, and print it on the screen if
        user_info.VERBOSE is True '''
    
    log_string = str(to_log)
    log_file = open("log.txt", 'a')
    time_str = time.strftime("%a,%d-%b-%Y~%H:%M ")
    log_file.write(time_str + log_string + "\n")
    log_file.close()
    if VERBOSE: print(log_string)