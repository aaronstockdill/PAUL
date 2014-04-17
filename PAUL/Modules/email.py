'''
email.py
Check unread mail with Paul.
Author: Aaron Stockdill
'''

import imaplib, email, smtplib

import paul

class Mailbox(object):
    ''' A simple representation of a mailbox for PAUL '''
    
    def __init__(self, provider):
        ''' Provide a simple mailbox for this provider '''
        self.kind = provider
        self.in_url = self.get_url("in")
        self.out_url = self.get_url("out")
        self.in_port = "993"
        self.out_port = "587"
        self.incoming = imaplib.IMAP4_SSL(self.in_url, self.in_port)
        # self.outgoing = smtplib.SMTP_SSL(self.out_url, self.out_port)
        # server.set_debuglevel(0)
        # self.outgoing.ehlo()
        #self.login()
        # self.outgoing.connect(self.out_url, self.out_port)
        

    def read_message(self, num):
        ''' Read the message num '''
        typ, data = self.incoming.fetch(num, '(RFC822)')
        message = email.message_from_string(str(data[0][1], encoding='utf8'))
        messages = message.walk()
        options = {"plain": None, "html": None}
        for m in messages:
            if m.get_content_type() == "text/plain":
                options["plain"] = m.get_payload()
            elif m.get_content_type() == "text/html":
                options["html"] = m.get_payload()
        paul.interact(options["plain"] if options["plain"] else "I can't really understand this email, you'll have to read it yourself later. Sorry.")
    
    
    def get_unread(self):
        self.incoming.select()
        typ, data = self.incoming.search(None, 'UnSeen')
        if str(data[0], encoding='utf8') == "":
            return ("You have no new messages.")
        else:
            num = str(data[0], encoding='utf8').split()
            r = paul.interact(
                              "You have {} unread message{}. ".format(
                                      len(num), 
                                      "s" if len(num) != 1 else ""
                              )
                              + "Do you want me to read {}?".format(
                                  "them" if len(num) != 1 else "it"
                              ),
                              response="y_n")
            if r:
                for n in num:
                    self.read_message(n)
            else:
                return "Ok."
    

    def get_url(self, in_out="in"):
        ''' Determine the url to use for a given provider '''
        if in_out == "in":
            if self.kind.lower() == "icloud":
                return 'p07-imap.mail.me.com'
            elif self.kind.lower() == "gmail":
                return 'imap.gmail.com'
        elif in_out == "out":
            if self.kind.lower() == "icloud":
                return 'smtp.mail.me.com'
            elif self.kind.lower() == "gmail":
                return 'smtp.gmail.com'
    
    
    def login(self, username, password):
        self.incoming.login(username, password)
        self.outgoing.login(username, password)
    
    
    def close(self):
        self.incoming.close()
        self.incoming.logout()
        self.outgoing.quit()


mb = None

def process(sentence):
    ''' Process the sentence '''
    global mb
    username = ''
    password = ''
    provider = ''
    if not mb:
        try:
            mb = Mailbox(provider)
        except ConnectionRefusedError:
            return "Oh no! Check your settings, I couldn't connect for some reason."
        try:
            mb.login(username, password)
        except:
            return "Hmmm... Check your username and password are correct."
    keywords = sentence.keywords(include=["VB"])
    paul.log("KEYWORDS:", keywords)
    if paul.has_one_of(keywords, ["read", "check", "have"]):
        r = mb.get_unread()
        return r if r else ""
    elif paul.has_one_of(keywords, ["write", "send", "compose"]):
        return "I can't quite do that yet. Working on it!"



def main():
    ''' The main function '''
    
    words = {
        "check": ("email", "verb"),
        "email": ("email", "noun"),
        "read": ("email", "verb"),
        "message": ("email", "noun"),
    }
    
    paul.associate(words)
    paul.register("email", process)

main()