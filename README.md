#PAUL
##Natural Language Assistant

###1. What is Paul?

Paul is a simple attempt at a system that can do something useful given a sentence, a natural language assistant. He works by deciding what types of words were said, and then dealing with the sentence based on the nouns.

###2. Technologies in Paul

Given I only speak english, it is English only. Given it is written in python and applescript, it is Mac OS X only. It uses mdfind, the command line version of spotlight, to find files. Using OS X's dictation it is possible to talk to Paul, too!

###3. Paul's Structure

The entry points are:

1. paul, a command line app that takes the sentence as it's argument. Good for a one-off command so you don't need the whole system.
2. cli.py, the main interface to have a conversation with paul. Does not exit after one command like above
3. gui.py, a tkinter GUI for cli.py

Modules are stored in Modules/, and extend Paul's functionality. So far there are only finder (file handling), discover (general knowledge from Wolfram Alpha) and weather (Yahoo weather).

Brain2 is the most modern brain. Brain was kind of shitty. It was much more stable, however. So if all you want is simple music control without much else, inside the cli.py and gui.py files, uncomment the line about importing brain, and comment out the brain2 and importer lines.

###4. Extending Paul

There is no API or anything in any real way, but the best system is this:

1. import user_info, this module has necessary globals
2. The process(sentence) function as the entrypoint from paul's brain. Is passed a list of tuples, with the most basic form of a word, and it's kind.
3. The main function has three statements:
 1. known\_nouns = {*noun*: lambda sentence: process(sentence),}, with noun changed. The rest is always the same.
 2. user\_info.nouns\_association.update(known\_nouns)
 3. if user\_info.VERBOSE: print("Successfully imported", \_\_name\_\_)
4. Call main, outside anything else. That way, when it is loaded, it will do the necessary setup.

Once this is done, you can either manually add your module to importer.py, or just run loader.py

Avoid printing anything without checking for user\_info.VERBOSE first. It is easier to switch a flag than it is to find and remove every print statement. Don't print information useful to the user, as it you cannot know how it will be presented, through the command line or the gui.

###5. Coming Soon?

Not so much a roadmap as a wishlist:

* Verb-based decisions too. If no nouns lead to somewhere, Paul should try and use the verbs to work out what is happening. E.g. so far finder has some hard-coded exceptions to the nouns rule. Why should it be special? let all apps add to a global 'verb dict' like the nouns do. We already handle verbs pretty good with the built-ins.
* Speaking Paul. Hopefully this will be coming sooner rather than later, as it is quite simple.
* Better weather. Sure, today's weather is nice, but if you ask for tomorrow's weather, you get todays too. I need to know!
* Reminders, events, time etc. This would be GREAT, but probably rather tricky.
* An alternative to Wolfram Alpha would be nice, to get text results back, but nothing else comes close. Damn. Probably not happening.
* Music controls. Basically the only thing version 1 *could* do, this one cannot.
* Brightness and volume (general system) controls. It'd be nice, hopefully not to difficult.