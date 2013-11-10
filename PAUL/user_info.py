"""
user_info.py
This is the 'global variable' storage, to share between all the 
different functions. Unfortunately, necessary given the current
designs. It also houses a few functions that do not play nice in other functions.
Author: Aaron Stockdill
"""

import time

## Global info that all systems should use. 
#  woeid is your WOEID (Yahoo weather location id).
#  name is what the computer will call you.
#  title is whether you can be addressed as sir or ma'am
#  it is whatever 'it' could be, changes automatically, DON'T touch.
#  temp: Use F for Fahrenheit, C for Celcius.
#  search_engine can be Google, Bing, Yahoo, DuckDuckGo or Baidu.
#  prompt is the little thing in front of what you type in, e.g. "?".
#  version is what version of Paul is being run.
info = {
    "woeid": "2348327",
    "name": "Aaron",
    "title": "sir",
    "it": None,
    "temp": "C",
    "search_engine": "Google",
    "prompt": "?",
    "version": "0.2.4",
}

## Flags for the system. 
#  Verbose is for debug info, 
#  noisy for paul to talk,
#  server is for the server to switch, don't touch it.
#  max_log_size is the maximum number of lines allowed in the log file.
#  first_run will let Paul know if he needs to do setup. Not yet implemented.
flags = {
    "VERBOSE": True,
    "NOISY": False,
    "SERVER": None,
    "MAX_LOG_SIZE": 2000,
    "LOGGING": True,
    "FIRST_RUN": False,
}