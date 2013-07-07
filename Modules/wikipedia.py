"""
wikipedia.py
Search wikipedia for information on a certain topic.
Author: Aaron Stockdill
"""

import urllib.request
import re
import os

import user_info
import brain2

def stripIt(s):
    ''' remove useless stuff '''
    txt = re.sub('<[^<]+?>', '', s)
    txt = re.sub('\[(\d)+\]', '', txt)
    txt = re.sub('&#160;', '', txt)
    return re.sub('\s+', ' ', txt)

def findIt(what):
    ''' Get wikipedia's opening statement on the topic '''
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = ('http://en.wikipedia.org/wiki/{}'.format(re.sub(' ', '_', what)))
    try:
        user_info.log("URL ATTEMPT: " + url)
        infile = opener.open(url)
        page = [str(line, encoding='utf8').strip() for line
                in infile.readlines()]
        
        content_start = page.index([line for line in page
                             if line.startswith("</table")][0])
        index1 = page.index([line for line in page[content_start:]
                             if line.startswith("<p")][0])
    
        user_info.info['it'] = url
        return stripIt(''.join(page[index1])) + "\n\n" + url
    except urllib.error.HTTPError:
        return brain2.forward(sentence, "wolfram")
    except urllib.error.URLError:
        return "I couldn't complete the research for some reason!"
    
def process(sentence):
    ''' Process the sentence '''
    
    sentence.replace_it()
    
    keywords = sentence.keywords()
    user_info.log("KEYWORDS: " + str(keywords))
    
    ignores = ["i", "wikipedia"]
    filtered_keywords = [word for word in keywords if word[0] not in ignores]
    
    brain2.loading()
    if filtered_keywords == []:
        return "I don't understand. Sorry!"
    return findIt(filtered_keywords[0][0])

def main():
    ''' The Main function '''
    
    words = {
        "wikipedia": ("wikipedia", "noun"),
        "tell": ("wikipedia", "verb"),
        "research": ("wikipedia", "verb"),
        "define": ("wikipedia", "verb"),
        "search": ("wikipedia", "verb"),
        "about": ("wikipedia", "preposition"),
        "find": ("wikipedia", "verb"),
    }

    user_info.associate(words)
    user_info.word_actions["wikipedia"] = lambda sentence: process(sentence)

    user_info.log("Successfully imported " + __name__)

main()