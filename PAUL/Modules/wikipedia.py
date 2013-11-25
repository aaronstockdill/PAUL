"""
wikipedia.py
Search wikipedia for information on a certain topic.
Author: Aaron Stockdill
"""

import urllib.request
import re
import os

import paul

def stripIt(s):
    ''' remove useless stuff '''
    txt = re.sub('<[^<]+?>', '', s)
    txt = re.sub('\[(\d)+\]', '', txt)
    txt = re.sub('&#160;', '', txt)
    return re.sub('\s+', ' ', txt)


def scrape_first_paragraph(url):
    ''' Get the first paragraph of the specified (print-formatted) 
        wikipedia article '''
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent',
                          'PAUL/{}'.format(paul.get_version()))]
    gross_url = url.replace("/wiki/", "/w/index.php?title=")+"&printable=yes"
    
    paul.log("URL ATTEMPT: " + gross_url)
    infile = opener.open(gross_url)
    page = [str(line, encoding='utf8').strip() for line
            in infile.readlines()]
    
    content_start = page.index([line for line in page
        if line.startswith("<div id=\"mw-content-text\"")][0])
    para = ''.join(page[content_start:]).split("<p>")[1].split("</p>")[0]
   
    paul.set_it(url)
    para = stripIt(para)
    if para.endswith("may refer to:"):
        paul.run_script("open {}".format(url))
        return "This is a diambiguation page. I'll bring it up now..."
    return para + "\n\n" + url


def findIt(what, sentence):
    ''' Get wikipedia's opening statement on the topic '''
    
    url = ('http://en.wikipedia.org/wiki/{}'.format(re.sub(' ', '_', what)))
    try:
        result = scrape_first_paragraph(url)
        return result
    except urllib.error.HTTPError:
        if sentence.forward("discover"):
            return "I'll try something else, just a moment..."
        else:
            return "I found nothing!"
    except urllib.error.URLError:
        return "I couldn't complete the research for some reason. Are you connected to the internet?"



def process(sentence):
    ''' Process the sentence '''
    
    sentence.replace_it()
    
    keywords = sentence.keywords()
    paul.log("KEYWORDS: " + str(keywords))
    
    ignores = ["i", "wikipedia"]
    filtered_keywords = [word for word in keywords if word[0] not in ignores]
    
    paul.loading()
    if filtered_keywords == []:
        return "I don't understand. Sorry!"
    return findIt(filtered_keywords[0][0], sentence)



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

    paul.associate(words)
    paul.register("wikipedia", process)

main()