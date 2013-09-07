#PAUL apha-0.1
##Natural Language Assistant
[View Website](http://aaronstockdill.github.io/paul.html)

###1. What is Paul?

Paul is a simple attempt at a system that can do something useful given a sentence, a natural language assistant. He works by deciding what types of words were said, and then dealing with the sentence based on the words. Given I only speak english, PAUL is English only. 

###2. Technologies in Paul

As PAUL is written in Python3 and Applescript, it is Mac OS X only. It uses mdfind, the command line version of spotlight, to find files. Using OS X's dictation it is possible to talk to Paul, too!

###3. Paul's Structure

PAUL is run in the following way:

    $ ./bin/PAUL [query]

If no query is provided, you enter 'discussion mode' where you can continually interact with Paul, and he keeps track of the conversation. For example, in discussion mode, if you just asked Paul to find some file for you, you would then just say "open that", or something of the sort, and he would. If you are not 
 
Modules are stored in PAUL/Modules/, and extend Paul's functionality. These are built using the paul API via `import paul`.

###4. Extending Paul

Paul is designed to be completely extendable. This is done through modules.

There is a more detailed guide at the bottom of this README [here](#building-paul-modules).

###5. Coming Soon?

Not so much a roadmap as a wishlist:

* Reminders, events, etc. This would be GREAT, but probably rather tricky.
* Deeper music controls. Basic play and pause stuff is nice, but song requests, shuffle, all that sort of thing, could be so much better!
* Brightness and volume (general system) controls. It'd be nice, hopefully not to difficult.
* Conversational interaction. If you say something that isn't an instruction, PAUL gives back a generic acknowledgement. Something more relevant would be good. At this time, the plan is an ineraction module.
* A weighted word association system. Not all words give the same information about which module it should be. For example, the weather module knows the days of the week, but so does the clock. Both score 1 point on "Is it Friday?", so which module gets used run is essentially random, and it can be tricky for the module to tell if it really is what was wanted, there are no clear hints that this is the wrong module from the words alone. If the words were weighted, it would be better. For example, using the day of the week in a sentence isn't actually that likely to be about the weather, it would have a low weighting for that module, but it is important to anything about a clock, so it would have a high weighting for that module. So it would be more like 0.7: clock.py and 0.3: weather -- clearly clock wins.

##Building PAUL Modules

PAUL is designed to be extended. When creating a module, most of it is up to use. You will be using whatever technologies you like as long as they are available on a standard Mac OS X system, as well as Python 3 itself, which PAUL is written in.

###Basic Setup

The first thing is to do the basic setup:

    import paul
    
    NOUNS = [known nouns]   # These can be non-global if desired, but it can
    VERBS = [known verbs]   # be useful if they are needed for 'ignore' lists.
    
    def process(sentence):
        # The stuff you want to do
    
    def main():
        words = {word: ("*module_name*", "noun") for word in NOUNS}
        words.update({word: ("*module_name*", "verb") for word in VERBS})
        ## update words with any other known words here too
        
        paul.associate(words)
        paul.vocab.word_actions["*module_name*"] = lambda sentence: process(sentence)
        
        paul.log("Successfully imported " + __name__)
    
    main()

Inside this template, you need to add some key things. Notably, you need AT LEAST one NOUN item (the word you program will know, e.g. "rain").
    
You should add all the words you know how to deal with, for both nouns and verbs (other word types are not very useful in making a decision - you can use other word types later, just do not rely upon them being there.)

###The Module itself.

Now you need something in the process(sentence) function. A sentence object is given to you, with an internal structure in the form:

    [('what', 'WH'), ('be', 'VB'), ('the', 'AR'), ('weather', 'NO'), ('like', 'PP'), ('today', 'NO')]
    
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

    list_of_part = sentence.get_part(tag, [indexes=False, prepositions=False])

For interacting with the user (if you want a repsonse, make it obvious how you want the reply, e.g. a list of a few options, or clearly a yes/no question, then set response to either "list" or "y\_n"):

    user_response = paul.interact(question, [response=None])
    
For a generic reply:

    paul.acknowledge()

If you need to provide a way to say you are working but there is no immediate response:

    paul.loading()

If your module has the potential to handle an 'it', such as a previously found url, file, or something else, use this method at the top of processing:

    sentence.replace_it()

To log anything, use the `paul.log(to_log)` function, passing a what you want logged in the string. If the VERBOSE flag is set in user\_info, it will be shown on the screen. It is always logged to log.txt. You can pass as many items as you want, they will be converted to a string and logged, separated by a space.

More API functions tend to be added over time (as I find I need them). The rest is basically up to you, using standard Python programming, using the os module to execute applescript or other stuff as necessary. It's basically anything goes! Be as creative as you can, be it X10 Home Automation, jokes, or something else you've dreamed up!

###Installing your Module

When your module is ready to go, drop it in to the Modules directory, and ask Paul to reload the modules. It really is that easy. 