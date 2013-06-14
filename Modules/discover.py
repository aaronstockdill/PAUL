import os
import user_info
from urllib.parse import quote

def process(sentence):
    query = "+".join([word[0] for word in sentence])
    os.system("open http://www.wolframalpha.com/input/?i=" 
               + quote(query).replace("%2B", "+"))

def main():
    if user_info.VERBOSE: print("Successfully imported", __name__)

main()