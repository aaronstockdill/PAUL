"""
user_info.py
This is the 'global variable' storage, to share between all the 
different functions. Unfortunately, necessary given the current
designs. It also houses a few functions that do not play nice in other functions.
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

## Flags for the system. 
#  Verbose is for debug info, 
#  noisy for paul to talk,
#  server is for the server to switch, don't touch it
VERBOSE = True
NOISY = False
SERVER = False