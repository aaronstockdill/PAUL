"""
user_info.py
This is the 'global variable' storage, to share between all the 
different functions. Unfortunately, necessary given the current
designs.
Author: Aaron Stockdill
"""

## Global info that all systems should use. 
info = {
    "woeid": "2348327", # Your WOEID (Yahoo weather location id)
    "name": "Master", # Your Name
    "computer": "paul", # Name of the computer system.
    "it": None, # Whatever 'it' could be
}

## Flags for the system. Verbose is for debug info, noisy for paul to talk
VERBOSE = True
NOISY = False

## Lists that get updated with what to do with each word
nouns_association = {}
verbs_association = {}