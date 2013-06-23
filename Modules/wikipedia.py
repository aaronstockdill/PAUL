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
    txt = re.sub('\[(\d)\]', '', txt)
    txt = re.sub('&#160;', '', txt)
    return re.sub('\s+', ' ', txt)

def findIt(what):
    ''' Get wikipedia's opening statement on the topic '''
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = ('http://en.wikipedia.org/w/index.php?title='
          '{}&printable=yes'.format(re.sub(' ', '_', what)))
    url2 = ('http://en.wikipedia.org/wiki/{}'.format(re.sub(' ', '_', what)))
    infile = opener.open(url)
    page = [str(line, encoding='utf8').strip() for line in infile.readlines()]
    index1 = page.index([line for line in page if line.startswith('<p')][0])
    #index2 = page.index([line for line in page if line.startswith('<p')][1])
    
    user_info.info['it'] = url2
    return stripIt(''.join(page[index1])) + "\n\n" + url2
    
def process(sentence):
    ''' Process the sentence '''
    
    keywords = brain2.group_together(sentence)
    if user_info.VERBOSE: print("KEYWORDS:", keywords)
    
    ignores = ["i", "wikipedia"]
    filtered_keywords = [word for word in keywords if word[0] not in ignores]
    
    brain2.loading()
    return findIt(filtered_keywords[0][0])

def main():
    ''' The Main function '''
    
    known_nouns = {
        "wikipedia": lambda sentence: process(sentence), 
    }

    known_verbs = {
        "tell": lambda sentence: process(sentence),
        "research": lambda sentence: process(sentence),
        "define": lambda sentence: process(sentence),
        "search": lambda sentence: process(sentence),
    }

    user_info.nouns_association.update(known_nouns)
    user_info.verbs_association.update(known_verbs)

    if user_info.VERBOSE: print("Successfully imported", __name__)

main()