#P.A.U.L. alpha-0.4
##Natural Language Assistant
[View Website](http://aaronstockdill.github.io/paul.html)

###1. What is Paul?

Paul is a simple attempt at a system that can do something useful given a sentence, a natural language assistant. He works by deciding what types of words were said, and then dealing with the sentence based on the words. Given I only speak english, PAUL is English only. 

###2. Technologies in Paul

As Paul is written in Python3 and Applescript, it is Mac OS X only. It uses mdfind, the command line version of spotlight, to find files. Using OS X's dictation it is possible to talk to Paul, too, using the command line interface.

###3. Installing Paul

~~The `install` script has not been tested. Run this at your own peril. No responsibility will be taken for loss of Paul, data, or a working operating system.~~ This `install` script __DOES NOT WORK__. Please __DO NOT USE IT__.

Paul has the functionality in place for a 'first run setup' interface, so on first run, please click "New User". Paul will then guide you through the set-up, and provide a quick run-down on how to interact with him.

###4. Paul's Structure

Paul is run from inside his directory in the following way:

    $ ./bin/paul [query]

If no query is provided, you enter 'discussion mode' where you can continually interact with Paul, and he keeps track of the conversation. For example, in discussion mode, if you just asked Paul to find some file for you, you would then just say "open that", or something of the sort, and he would. If you are not in discussion mode, Paul has no recollection of previous statements.
 
Modules are stored in PAUL/Modules/, and extend Paul's functionality. These are built using the paul API via `import paul`.

###5. Extending Paul

Paul is designed to be completely extendable. This is done through modules.

There is a more detailed guide at the bottom of this README [here](#building-paul-modules).

###6. Coming Soon?

Not so much a roadmap as a wishlist:

* Reminders, events, etc. This would be GREAT, but probably rather tricky.
* ~~Deeper music controls. Basic play and pause stuff is nice, but song requests, shuffle, all that sort of thing, could be so much better!~~ Partially implemented, but could still be improved greatly.
* A weighted word association system. Not all words give the same information about which module it should be. For example, the weather module knows the days of the week, but so does the clock. Both score 1 point on "Is it Friday?", so which module gets used run is essentially random, and it can be tricky for the module to tell if it really is what was wanted, there are no clear hints that this is the wrong module from the words alone. If the words were weighted, it would be better. For example, using the day of the week in a sentence isn't actually that likely to be about the weather, it would have a low weighting for that module, but it is important to anything about a clock, so it would have a high weighting for that module. So it would be more like 0.7: clock.py and 0.3: weather -- clearly clock wins.
* Social Networking, and using Facebook user seach as a type of 'who is' system: "https://www.facebook.com/search/results.php?q={}&type=users" should work well. Full on "PA Social Presence" will be much trickier.

* * *

##Building PAUL Modules

Paul is designed to be extended. When creating a module, most of it is up to you. You will be using whatever technologies you like as long as they are available on a standard Mac OS X system, as well as Python 3 itself, which Paul is written in.

###Basic Setup

The first thing is to do the basic setup:

    import paul
    
    NOUNS = [known nouns]   # These can be non-global if desired, but it can
    VERBS = [known verbs]   # be useful if they are needed for 'ignore' lists.
    
    def process(sentence):
        # The stuff you want to do
        return answer # Return what you want to say to the user
    
    def main():
        words = {word: ("*module_name*", "noun") for word in NOUNS}
        words.update({word: ("*module_name*", "verb") for word in VERBS})
        ## update words with any other known words here too
        
        paul.associate(words)
        paul.register("*module_name*", process)
    
    main()

Inside this template, you need to add some key things. Notably, you need AT LEAST one NOUN item (the word you program will know, e.g. "rain").
    
You should add all the words you know how to deal with, for both nouns and verbs (other word types are not very useful in making a decision - you can use other word types later, just do not rely upon them being there.)

###The Module itself.

Now you need something in the process(sentence) function. A sentence object is given to you, with an internal structure in the form:

    [('what', 'WH'), ('be', 'VB'), ('the', 'AR'), ('weather', 'NO'), ('like', 'PP'), ('today', 'NO')]
    
As you can see, the word is reduced to its most basic form (the sentence is from the query "What's the weather like today?") - "is" became "be". The tags are:

* N\* for nouns, with O for object, S for subject after the N.
* P\* for pronouns, same suffixes as above.
* X\* for names (mostly your name, and 'it'), same suffixes.
* VB for verbs.
* PP for prepositions.
* NU for numbers.
* AR for articles.
* WH for question words.
* ?? for unknown words.

Given all this information it is up to you to use it. Some functions are provided in `paul` for your use. For easily accessing the parts of the sentence:

    list_of_part = sentence.get_part(tag, [indexes=False, prepositions=False])

For interacting with the user (if you want a repsonse, make it obvious how you want the reply, e.g. a list of a few options, or clearly a yes/no question, then set response to either "list" or "y\_n"):

    user_response = paul.interact(question, [response=None, end=True])
    
End specifies if this is the end of what Paul is currently saying. If you are providing some interim result, end must be False, or else the user may be offered a prompt, and this gets messy quickly.

For a generic reply:

    paul.acknowledge()

If you need to provide a way to say you are working but there is no immediate response:

    paul.loading()

If your module has the potential to handle an 'it', such as a previously found url, file, or something else, use this method at the top of processing:

    sentence.replace_it()
Or, to just get the current value of 'it': 

    paul.get_it()

If you need to set 'it', use the companion function:

    paul.set_it(value)

If your module needs to run a script, use this:

    paul.run_script(code, [language='bash', response=False])

The `code` parameter is rather self explanitory. The `language` paramenter is optional, and defaults to bash. Other values include python3, ruby, perl and applescript. Response is True or False, depending on whether you want the result. The result returned is what the code returned. If you are expecting multiple lines, split it by newline characters: `\n`

To log anything, use the `paul.log(to_log)` function, passing a what you want logged in the string. If the VERBOSE flag is set in user\_info, it will be shown on the screen. It is always logged to log.txt. You can pass as many items as you want, they will be converted to a string and logged, separated by a space. E.g. paul.log("TITLE:", "hello") => "TITLE: hello"

More API functions tend to be added over time (as I find I need them). A full run-down of every function is in the README of the PAUL directory. The rest is basically up to you, using standard Python programming, using the os module to execute applescript or other stuff as necessary. It's basically anything goes! Be as creative as you can, be it X10 Home Automation, jokes, or something else you've dreamed up!

###Installing your Module

When your module is ready to go, drop it in to the Modules directory, and ask Paul to reload the modules. It really is that easy. 

***

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.