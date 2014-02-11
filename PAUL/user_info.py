"""
user_info.py
This is the 'global variable' storage, to share between all the 
different functions. Unfortunately, necessary given the current
designs.

THIS FILE IS MARKED FOR DELETION. PLEASE USE THE NEW paul.system MODULE.

Author: Aaron Stockdill
"""

## Global info that all systems should use. YOU CAN CHANGE THESE CAREFULLY
#  woeid is your WOEID (Yahoo weather location id).
#     Go to weather.yahoo.com to find your city, then
#     copy the last number in the url to woeid here.
#  name is what the computer will call you.
#  title is whether you can be addressed as sir or ma'am
#  temp: Use F for Fahrenheit, C for Celcius.
#  search_engine can be Google, Bing, Yahoo, DuckDuckGo or Baidu.
#  prompt is the little thing in front of what you type in, e.g. "?".
#  version is what version of Paul is being run.
info = {
    "woeid": "2348327",
    "name": "Aaron",
    "title": "sir",
    "temp": "C",
    "search_engine": "Google",
    "prompt": "?",
}

## Flags for the system. DO NOT TOUCH ANY OF THESE
#  Verbose is for debug info, 
#  noisy for paul to talk,
#  max_log_size is the maximum number of lines allowed in the log file.
#  first_run will let Paul know if he needs to do setup. Not yet implemented.
#  it is whatever 'it' could be, changes automatically.
#  send is the function that is used to send data to the user.
#  get is the function that is used to get data from the user.
#  exec is the function that is used to send executable scripts to the user.
flags = {
    "VERSION": "0.3.2",
    "VERBOSE": True,
    "NOISY": False,
    "MAX_LOG_SIZE": 500,
    "LOGGING": True,
    "FIRST_RUN": False,
    "IT": None,
    "SEND": None,
    "GET": None,
    "EXEC": None,
}
