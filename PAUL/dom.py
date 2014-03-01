"""
dom.py
Author: Aaron Stockdill

Breaking DOM into its own file. Hopefully this will keep things a little more
organised. also hides Element better, as this is not something for people to 
use.
"""

import urllib.request
import Settings.system as system

def get_version():
    ''' Returns the current version of Paul as a string '''
    return system.flags["VERSION"]

class Element(object):
    ''' A simple element object for the DOM parser '''

    def __init__(self, tag_code):
        ''' Initialise with tag name and attributes '''
        self.code = tag_code
        self.tag = self.get_name()
        self.children = []
        self.attributes = self.get_attributes()


    def __str__(self):
        return "({}, {})".format(self.tag, str(self.children))


    def __repr__(self):
        return self.__str__()


    def __getitem__(self, i):
        ''' Get item via slice notation, changes based on input '''
        if type(i) == int:
            return self.children[i]
        elif i[0] == "#":
            return self.get_id(i[1:])
        elif i[0] == ".":
            c = self.get_class(i[1:])
            return c if c != [] else None
        else:
            return self.get_elem(i)


    def get_id(self, target):
        ''' Get the element with id "target" recursively, return
            the first suitable element '''

        if self.attributes.get("id", None) == target:
            return self
        else:
            for c in self.children:
                try:
                    e = c['#{}'.format(target)]
                    if e:
                        return e
                except TypeError:
                    pass
        return None


    def get_class(self, target):
        ''' Get the elements with class "target" recursively, return
            a list of suitable elements '''

        result = []
        if self.attributes.get("class", None) == target:
            result += [self]
        for c in self.children:
            try:
                e = c['.{}'.format(target)]
                if e:
                    result += e
            except TypeError:
                pass
        return result


    def get_elem(self, target):
        ''' Get the element "target" recursively, return a list of suitable
            elements '''

        result = []
        if self.tag == target:
            result += [self]
        for c in self.children:
            try:
                e = c['{}'.format(target)]
                if e:
                    result += e
            except TypeError:
                pass
        return result


    def get_name(self):
        ''' Try and get the name of the tag '''

        try:
            return self.code.split()[0][1:].lower().strip(">")
        except IndexError:
            print ("'{}'".format(self.code))


    def get_parts(self, string):
        ''' Extract the parts of the element tag, the attributes. '''

        parts = {}
        key = ""
        value = ""
        encloser = None
        for char in string.strip():
            if char == "=":
                key = value
                value = ""
            elif char == "'":
                if encloser == "'":
                    parts[key] = value
                    encloser = None
                    key = ""
                    value = ""
                elif encloser:
                    value += char
                else:
                    encloser = "'"
            elif char == '"':
                if encloser == '"':
                    parts[key] = value
                    encloser = None
                    key = ""
                    value = ""
                elif encloser:
                    value += char
                else:
                    encloser = '"'
            elif char == " ":
                if encloser:
                    value += char
                elif key != "":
                    parts[key] = value
                    key = ""
                    value = ""
                else:
                    parts[key] = value
                    key = ""
                    value = ""
            else:
                value += char
        try:
            del parts[""]
        except KeyError:
            pass
        return parts


    def get_attributes(self):
        ''' Try and get attributes of element, e.g. id and class '''

        c = self.code.strip().strip(">").strip("<")
        c = " ".join(c.split()[1:])
        parts = self.get_parts(c)
        return parts


    def get_immediate_child(self, target):
        ''' Useful if you only want immediate children of an element,
            not EVERY child of an element. '''

        if target[0] == "#":
            for c in self.children:
                try:
                    if c.attributes["id"] == target[1:]:
                        return c
                except TypeError:
                    pass
        elif target[0] == ".":
            result = []
            for c in self.children:
                try:
                    if c.attributes["class"] == target[1:]:
                        result += [c]
                except TypeError:
                    pass
            return result
        else:
            result = []
            for c in self.children:
                try:
                    if c.tag == target:
                        result += [c]
                except AttributeError:
                    pass
            return result


    def extract_raw_text(self):
        ''' Extract out raw text, so there are no tags or anything. '''

        out = ""
        for c in self.children:
            if type(c) == Element:
                out += c.extract_raw_text()
            else:
                out += c
        return out



class DOM(object):
    ''' Create a DOM, and work with it. Useful to parse HTML '''

    def __init__(self, html):
        ''' Create the DOM from the html '''
        self.code = html
        self.tokens = self.tokenize(html)
        self.dom = self.domify(self.tokens)


    @classmethod
    def fromURL(self, url):
        ''' Create a new DOM object from a given URL '''
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent',
                              'PAUL/{}'.format(get_version()))]
        infile = opener.open(url)
        page = str(infile.read(), encoding='utf8')
        newDOM = DOM(page)
        return newDOM


    def __getitem__(self, key):
        ''' Nice access straight to the DOM. '''
        return self.dom[key]


    def __str__(self):
        ''' Pretty-print DOM '''
        return str(self.dom)


    def remove_non_html(self, tokens):
        ''' Remove scripts and styles '''

        cont = True
        j = 0
        new_tokens = []
        while cont:
            tag = tokens[j]
            try:
                tag_name = tag.split()[0].strip(">").strip("<")
            except:
                tag_name = "  "
            if tag_name in ["style", "script"]:
                cont2 = True
                if tag_name == "script" and tag[-2:] == "/>":
                    pass # Ignore it
                else:
                    while cont2:
                        try:
                            tag_name2 = tag.split()[0].strip(">").strip("<").strip("/")
                        except:
                            tag_name2 = "  "
                        if tag_name2 == tag_name:
                            cont2 = False
                        j += 1
            else:
                if not (tag in ["</style>", "</script>"]):
                    new_tokens.append(tag)
            j += 1
            if j == len(tokens):
                cont = False
        return new_tokens


    def tokenize(self, code):
        ''' Turn the code into tokens '''

        tokens = []
        i = 0
        for char in code:
            if char == "\n":
                pass
            elif char == ">":
                tokens[i] += char
                i += 1
            elif char == "<":
                if (i+1) == len(tokens):
                    i +=1
                tokens.append(char)
            else:
                try:
                    tokens[i] += char
                except IndexError:
                    tokens.append(char)

        return self.remove_non_html(tokens)


    def domify(self, tokens):
        ''' Parse the tokens into a DOM. '''

        def in_stack(tag, stack):
            for i in stack:
                if type(i) == str:
                    try:
                        if i.split()[0][1:] == tag or i.split()[0][1:-1] == tag:
                            return True
                    except IndexError:
                        pass
            return False

        stack = []
        detag = lambda a: a.split()[0].strip("<").strip(">")
        for t in tokens:
            try:
                tag_name = detag(t)
                tag_end = t[-2:]
            except:
                stack.append(t)
                continue
            if tag_name == "!DOCTYPE":
                pass
            elif tag_end == "/>":
                e = Element(t)
                stack.append(e)
            elif len(t) > 1 and t[1] == "/":
                alt = t[2:-1]
                if in_stack(alt, stack):
                    temp = []
                    cont = True
                    while cont:
                        try:
                            if (type(stack[-1]) == str):
                                if stack[-1].strip() == "":
                                    temp.append(" ")
                                    stack.pop()
                                elif detag(stack[-1]) == alt:
                                    cont = False
                                elif stack[-1][0] == "<" and stack[-1][-1] == ">" and detag(stack[-1]) != alt:
                                    temp.append(stack.pop())
                                    n = self.domify(temp)
                                    temp.append(n)
                                else:
                                    temp.append(stack.pop())
                            else:
                                temp.append(stack.pop())
                        except IndexError:
                            cont = False
                    try:
                        tag = stack.pop()
                    except IndexError:
                        pass
                    temp.reverse()
                    e = Element(tag)
                    e.children = temp
                    stack.append(e)
            else:
                stack.append(t)
        for item in stack:
            if isinstance(item, Element):
                return item
        return stack[0]