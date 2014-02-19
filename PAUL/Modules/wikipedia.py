"""
wikipedia.py
Search wikipedia for information on a certain topic.
Author: Aaron Stockdill
"""

import urllib.error
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
        
    gross_url = url.replace("/wiki/", "/w/index.php?title=")+"&printable=yes"
    paul.log("URL ATTEMPT: " + gross_url)
    d = paul.DOM.fromURL(gross_url)
    para = d["#mw-content-text"].get_immediate_child('p')[0].extract_raw_text()
   
    paul.set_it(url)
    para = stripIt(para)
    if para.endswith("may refer to:") or para.endswith("may refer to"):
        paul.open_URL(url)
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
    except AttributeError:
        paul.set_it(url)
        paul.open_URL(url)
        return "I can't seem to read about this. Let me open it for you..."



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
    if filtered_keywords[0][0] in ["joke", "jokes"]:
        if sentence.has_word("about"):
            pass
        else:
            return sentence.forward("personality")
    elif filtered_keywords[0][0].startswith("http"):
        paul.open_URL(filtered_keywords[0][0])
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