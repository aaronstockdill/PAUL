#P.A.U.L. alpha-0.3
### API Reference

####Contents

* [Laying out your Module](#laying-out-your-module)
* [log](#log)
* [update\_words](#update-words)
* [associate](#associate)
* [register](#register)
* [simple\_speech\_filter](#simple-speech-filter)
* [interact](#interact)
* [loading](#loading)
* [acknowledge](#acknowledge)
* [iterable](#iterable)
* [trim\_word](#trim-word)
* [has\_word](#has-word)
* [has\_one\_of](#has-one-of)
* [join\_lists](#join-lists)
* [filter\_unless\_listed](#filter-unless-listed)
* [filter\_out](#filter-out)
* [run\_script](#run-script)
* [set\_it](#set-it)
* [get\_it](#get-it)
* [get\_version](#get-version)
* [send\_notification](#send-notification)
* [parse\_number](#parse-number)
* [Sentence](#sentence)
  * [kind](#kind)
  * [\_\_repr\_\_](#--repr--)
  * [\_\_str\_\_](#--str--)
  * [\_\_iter\_\_](#--iter--)
  * [keywords](#keywords)
  * [get\_part](#get-part)
  * [clean](#clean)
  * [tag\_word](#tag-word)
  * [classify](#classify)
  * [tag\_sentence](#tag-sentence)
  * [replace\_it](#replace-it)
  * [forward](#forward)
  * [has\_word](#has-word-2)
  * [has\_one\_of](#has-one-of-2)

* * *

####Laying out your Module

A module is always started with the same basic framework:

    import paul
    
    def process(sentence)
        ''' Process the sentence '''
        # Do something useful
    
    def main():
        ''' The main function '''
        words = {word: ("module", "noun") for word in NOUNS}
        paul.associate(words)
        paul.register("module", process)
    
    main()

Replace `module` with the name of your module, and adjust the words dictionary to accurately represent the words your module should be associated with. `process` should return a string that serves as a reply from Paul as to what was done. This can be anything from "Ok" through to "The two week old raspberry jam from the local orchard has successfully been spread onto the artisan bread that was purchased from the market at 9:15 this morning." so long as it is meaningful to the user. Beyond this basic framework, it's up to you. The Paul API, as described below, has some useful functions for you to use.

* * *

####log
`paul.log(*to_log)` is used to log some data. If paul.user\_info.flags['LOGGING'] is True, this will be written to the file log.txt inside the same directory as this reference. If paul.user\_info.flags['VERBOSE'] is True, this data will also be shown in the terminal interface. This function will return True if the data was written to the file log.txt, otherwise it will return False, even if the data was written to the terminal interface. `paul.log(to_log)` actually takes as many arguments as you want, so long as they have a string representation. It converts all of these arguments to a string representation, and joins them, separated by a space. Log entries are written with a time and date in front of them. log.txt will remove items from the start of the log after is reaches  the size stated in paul.user\_info.flags['MAX\_LOG\_SIZE'].

* * *

####update\_words
Do not call this function. Paul will handle this.

* * *

####associate
`paul.associate(words_dict)` is used to associate words with your module in Paul's brain. The words_dict entries should be structured as such:

    "word": ("module", "word_type"),

where `word` is the word you wish to associate with your module, `module` is the name of your module, and `word_type` is the type of word you are registering -- noun or verb.

* * *

####register
`paul.register(module, function)` is used to register your module with the rest of Paul's brain. `module` is the string used above in associate to name your module. `function` will likely be called `process`, and must accept exactly one argument, the sentence.

* * *

####simple\_speech\_filter
Do not call this function. Paul will handle this.

* * *

####interact
`paul.interact(statement[, response=None, end=True])` is one of the most important functions in the whole API, simply because, after `paul.log`, it is one of the most used. This is the standard function for interacting with the user. It is called on any return value from `process` functions, and is your main way to get any information to or from the user outside of normal get-in-a-sentence, return-a-response. The only required argument is `statement`, which is what you want to say to the user, as a string. `response` defaults to None, but can also have "list", "y\_n" or "arb" strings passed into it. These change the behavior of the function:

* `list` assumes that the statement is a list of numbered options, and the user will reply with a the option they want. The function will return None if no number is found in their response, or an integer which details their response. You may need to deal with off-by-one errors, as people will ask for list item 0 by using words like "first" or "one", which will result in the function returning 1.
* `y_n` assumes the statement is a yes-no style question. Words that seem to be in the affirmative will return True, words in the negatives will return False, and if neither kind is found None is returned.
* `arb` means arbitrary. You have to deal with this, we will give you the raw string. If you want to handle it like any other sentence, use `sentence = paul.Sentence(returned_arb)`.

`end` defaults to True. This means that you're done talking to the user, and it is their turn to talk. Most of the time this is what you want, but if you have given a response that is interim, such as "Hang on a sec...", you don't want them talking again as you haven't given them what they asked for yet. In this case, set end to False. For functions like loading and acknowledge (see below) end is defaulting to False, as it is more likely that these are being used as a gap-fill while data is loading.

* * *

####loading
`paul.loading()` takes no arguments. It is designed to produce a simple response from Paul to let you know that he is thinking right now. The result is returned to you in case it is relevant.

* * * 

####acknowledge
`paul.acknowledge([end=False])` takes only one optional argument end (see `interact` for a description of this parameter) which defaults to True. It is designed to let the user know that you have heard them. There is no indication that anything is being done however, so if it is a loading filler, use `paul.loading()` instead. `paul.acknowledge()` can be used to respond to a user generally by returning an empty string from process as well, if you call this just before returning, as Paul ignores the response of modules that return None or "".

* * *

####iterable
`paul.iterable(item)` provides an easy way to tell if an item can be iterated over, but does not return true for a String. Returns True if the item is a list, tuple, dict or Sentence, False otherwise.

* * *

####trim\_word
`paul.trim_word(word_list, word)` is used to trim the word given as an argument from the list word\_list. If the word\_list contains sublists or tuples instead of strings, the entire sublist or tuple containing the word is removed. This function has an optional parameter that you must not tamper with, as it controls the recursion that this function uses.

* * *

####has\_word
`paul.has_word(word_list, word)` determines if the `word_list` contains the `word` given. Returns True if the word is found, False otherwise. This function is capable of searching any depth of nested lists for the word, so the word_list ["one", ["two", ["three", "four"], "five"], "six", "seven"] would be found to contain the word "four" with no difficulty. For searching sentences, use the sister-function inside the Sentence object.

* * *

####has\_one\_of
`paul.has_one_of(list_to_search, confirm_list)` searches for any of the words in `confirm_list` in `list_to_search` -- that is, if any of the words in the list `confirm_list` appear in the list `list_to_search`, this function will return True, otherwise it will return False. Like `paul.has_word`, this function will perform a recursive search. For searching sentences, use the sister-function inside the Sentence object.

* * *

####join\_lists
`paul.join_lists(*lists)` will join all the arguments that are lists together, and will return the new super_list. Any argument that is not a list is quietly ignored. The main benefit of this function is that it can join lists that may not all exist, for example if you requested a part of the sentence that doesn't happen to exist in this sentence, you would normally need to check each part to determine if it is not None, then join it. This is faster and easier.

* * *

####filter\_unless\_listed
`paul.filter_unless_listed(main_list, *rest)` is used to filter out a `main_list`, by removing any word that does not exist in the remaining list arguments. This is useful if you need to trim all the useless words from, for example, keywords. This function returns the new list.

* * *

####filter\_out
`paul.filter_out(main_list, *rest)` is used to filter out any words from the `main_list` that appear in the rest of the lists. For example, you get keywords, and you want to ignore some of your own associated words because they have very little actual meaning to you. The new list is returned.

* * *

####run\_script
`paul.run_script(code[, language='bash', response=False])` is used to execute a small helper script that you need the result of to carry on. This is the main way to interface with other applications, as Applescript provides a good way to communicate. The language parameter requests the language that your script is written in. It defaults to a standard bash script, i.e. terminal commands, but can take in applescript, ruby, python3 and perl. The response parameter defaults to False, meaning it will return None, as there is no need of a result. However, if there is a need of a result, set response to True. Then, `paul.run_script` will return the result of the code than ran.

* * *

####set\_it
`paul.set_it(value)` sets the global variable "it" to the value specified. You can store pretty much anything in there. It is useful for "context", for example the finder module can open "it", if you have just found a file. Returns the value of "it", just in case you need to see if it stuck.

* * *

####get\_it
`paul.get_it()` is used to get the value of "it". This can be useful, but it can be more useful to use the sister-function in sentence called `replace_it()`, which inserts it naturally into the sentence.

* * *

####get\_version
`paul.get_version()` returns the string describing what version of Paul is being run. Tends to be more useful for front-ends than modules, but may be necessary, for example the wikipedia module announces itself by this code.

* * *

####send\_notification
`paul.send_notification(title, message)` is used to send a system notification to the user, using the title and message supplied in the arguments. The title should **not** be your module name, it should be something useful. The same goes for the message.

* * *

####parse\_number
`paul.parse_number(string)` will extract a number from the string argument, returning an integer. It will quietly ignore everything it does not understant. If it encounters an actual digit, this is returned. If it encouters any lexical representaion of a number, it turns it into an integer, e.g. "forty two" => 42. 

* * *

####Sentence
`paul.Sentence(init_string)` is the class that is used to represent a sentence inside the brain and modules. Its internal structure is a series of tuples containing (word, type) pairs. For example, the `init_string` "What's the weather like today?" produces the following sentence object (obtained through the `__repr__()` method):

    [('what', 'WH'), ('be', 'VB'), ('the', 'AR'), ('weather', 'NO'), ('like', 'PP'), ('today', 'NO')]

Every word is reduced to its most basic form, and is tagged with the word type. However, this is not often the form you have to deal with it. Mostly, you interact with keywords in the sentence. Following are the methods available to the Sentence object.

#####kind
`Sentence.kind` is not a method, but a variable. This houses the kind of sentence it is: Imperative (IMP), Accusative (ACC) or Interogative (INT). Knowing these is not important, but you may want to know it all the same.

#####\_\_repr\_\_
This is not a function you will call often, but it is how python will reveal the sentence to you if queried in the interpreter. Shows the structure nicely. For example:

    >>> s = "what time is it"
    >>> s
    [('what', 'WH'), ('time', '??'), ('be', 'VB'), ('it', 'PO')]

#####\_\_str\_\_
Once again, not a function you will call often, but this is how the sentence will appear if asked to print it. Using the variable `s` from above:

    >>> print(s)
    what time is it

#####\_\_iter\_\_
Another function you need not call explicitly. It just enables you to use python's lovely `for` syntax to iterate over the word tuples in the sentence.

#####keywords
`Sentence.keywords([ignore=None, include=None])` is a method that you will never want to be without. This method examines the sentence, extracts keywords, and groups some together if they seem like they should be paired. It returns tuples, so that you know where the word came in the sentence, and so you can pair it with prepositions if need be. The return is of the form `[(keyword, index), ...]`. There are two optional arguments for this method: ignore, where you list words you explicitly want to ignore, and include, where you list word types that you definitely want included on top of the standard four -- ?? (unknowns), NO (objects), XO (names) and NU (numbers). This can be things such as NS (subjects), XS (names), or VB (verbs).

#####get\_part
`Sentence.get_part(part[, indexes=False, pronouns=False])` extracts the words in the sentence that are a certain word type, namely `part`. This can be any type of word that Paul can handle. Word types and their codes can be found in `vocab.py`. If `indexes` is True, the result will be a list of tuples, not a list of strings, with the second part of the tuple containing where in the sentence this word appeared. If `pronouns` is True, the method will allow words like "he", or "she", rather than just the names. If the method has already tried without success not including pronouns, it will try again with pronouns anyway. Only when that too has failed will it return None.

#####clean
This is a helper method that you do not need to touch. If you have a word that needs cleaning of extra characters, technically this will do it for you, but it is a bit odd.

#####tag\_word
Another helper method that you do not need to touch. If you need a word tagged, this can do it, but this is not what it was designed for.

#####classify
Classify the sentence. You should be able to simply query `Sentence.kind` and not have to call this method yourself.

#####tag\_sentence
A method you should not have to touch, this is run when the sentence is created so it is all ready to go for you.

#####replace\_it
`Sentence.replace_it()` is a method you will use relatively frequently. This searches the sentence for an occurence of "it", and subs in the value currently in the global memory. This function returns True if a substitution is made, False otherwise.

#####forward
`Sentence.forward(module)` is a method that will pass the Sentence onto another module. Use this is you think you may have recieved the Sentence in error. Return its value in place of any of your responses. 

#####has\_word
`Sentence.has_word(word)` is a method used to determine if a specific word has appeared in the sentence. This is equivalent to calling `paul.has_word(Sentence, word)`.

#####has\_one\_of
`Sentence.has_one_of(confirm_list)` is a method used to determine if any of the words confirm_list appear in the sentence. Equivalent to `paul.has_one_of(Sentence, confirm_list)`.