#PAUL
##Natural Language Assistant

###1. What is Paul?

Paul is a simple attempt at a system that can do something useful given a sentence, a natural language assistant. He works by deciding what types of words were said, and then dealing with the sentence based on the nouns. Given I only speak english, PAUL is English only. 

###2. Technologies in Paul

As PAUL is written in python 3 and applescript, it is Mac OS X only. It uses mdfind, the command line version of spotlight, to find files. Using OS X's dictation it is possible to talk to Paul, too!

###3. Paul's Structure

The entry points are:

1. paul, a command line app that takes the sentence as it's argument. Good for a one-off command so you don't need the whole system.
2. cli.py, the main interface to have a conversation with paul. Does not exit after one command like above.
3. gui.py, a tkinter GUI for cli.py

Modules are stored in Modules/, and extend Paul's functionality. So far there are only finder (file handling), discover (general knowledge from Wolfram Alpha) and weather (Yahoo weather).

Brain2 is the most modern brain. Brain was kind of shitty. It was much more stable, however. So if all you want is simple music control without much else, inside the cli.py and gui.py files, uncomment the line about importing brain, and comment out the brain2 and importer lines.

###4. Extending Paul

Paul is designed to be completely extendable. This is done through what

There is a more detailed guide at the bottom of this README [here]("#building-paul-modules").

###5. Coming Soon?

Not so much a roadmap as a wishlist:

* Verb-based decisions too. If no nouns lead to somewhere, Paul should try and use the verbs to work out what is happening. E.g. so far finder has some hard-coded exceptions to the nouns rule. Why should it be special? let all apps add to a global 'verb dict' like the nouns do. We already handle verbs pretty good with the built-ins. **UPDATE:** This is partially implemented. If no known nouns are found, it searches the knwon verbs, and uses them. Modules must be updated to use this new functionality.
* Better weather. Sure, today's weather is nice, but if you ask for tomorrow's weather, you get todays too. I need to know!
* Reminders, events, time etc. This would be GREAT, but probably rather tricky.
* An alternative to Wolfram Alpha would be nice, to get text results back, but nothing else comes close. Damn. Probably not happening.
* Music controls. Basically the only thing version 1 *could* do, this one cannot.
* Brightness and volume (general system) controls. It'd be nice, hopefully not to difficult.

##Building PAUL Modules

PAUL is designed to be extended. When creating a module, most of it is up to use. You will be using whatever technologies you like as long as they are available on a standard Mac OS X system, except Python 3 itself, which PAUL is written in.

###Basic Setup

The first thing is to do the basic setup:

    import user_info
    
    def process(sentence):
        # The stuff you want to do
    
    def main():
        known_nouns = {}
        known_verbs = {}
        
        user_info.nouns_association.update(known_nouns)
        user_info.verbs_association.update(known_verbs)
        
        if user_info.VERBOSE: print("Successfully imported", __name__)
    
    main()

Inside this template, you need to add some key things. Notably, you need AT LEAST one known\_noun key (the word you program will know, e.g. "rain"). All keys will have a value of:

    lambda sentence: process(sentence)
    
You should add all the words you know how to deal with, for both nouns and verbs (other word types are not very useful in making a decision - you can use other word types later, just do not rely upon them being there.)

###The Module itself.

Now you need something in the process(sentence) function. A sentence is given to you in the form:

    [('what', 'WH'), ('be', 'VB'), ('the', 'AR'), ('weather', 'NO'), ('like', 'PP'), ('today', '??')]
    
As you can see, the word is reduced to its most basic form (the sentence is from the query "What's the weather like today?") - "is" became "be". The tags are:

* N\* for nouns, with O for object, S for subject after the N.
* P\* for pronouns, same suffixes as above.
* X\* for names (mostly the computer name, your name, and 'it'), same suffixes.
* VB for verbs.
* PP for prepositions.
* OR for ordinals.
* AR for articles.
* WH for question words.
* ?? for unknown words.

Given all this information it is up to you to use it. Some functions are provided in brain2 for your use. For easily accessing the parts of the sentence:

    list_of_parts = brain2.get_parts(sentence, tag[, indexes=False, prepositions=False])

For interacting with the user:

    response = brain2.interact(question+options[, response=None])
    
For a generic reply:

    brain2.acknowledge()

More API functions tend to be added over time (as I find I need them). The rest is basically up to you, using standard Python programming, using the os module to execute applescript or other stuff as necessary. It's basically anything goes! Be as creative as you can, be it X10 Home Automation, jokes, or something else you've dreamed up!

###Installing your Module

When your module is ready to go, drop it in to the Modules directory, and ask Paul to reload the modules. It really is that easy. 