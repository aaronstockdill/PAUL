'''
email.py
Check unread mail with Paul.
Author: Aaron Stockdill
'''

import imaplib, email

import paul

class Mailbox(object):
    ''' A simple representation of a mailbox for PAUL '''
    
    def __init__(self, provider):
        ''' Provide a simple mailbox for this provider '''
        self.kind = provider
        self.url = self.get_url()
        self.port = "993"
        self.M = imaplib.IMAP4_SSL(self.url, self.port)
        

    def read_message(self, num):
        ''' Read the message num '''
        typ, data = self.M.fetch(num, '(RFC822)')
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
        self.M.select()
        typ, data = self.M.search(None, 'UnSeen')
        if str(data[0], encoding='utf8') == "":
            return ("You have no new messages.")
        else:
            num = str(data[0], encoding='utf8').split()
            r = paul.interact("You have {} unread messages. ".format(len(num))
                              + "Do you want me to read them?",
                              response="y_n")
            if r:
                for n in num:
                    self.read_message(n)
            else:
                return "Ok."
    

    def get_url(self):
        ''' Determine the url to use for a given provider '''
        if self.kind.lower() == "icloud":
            return 'p07-imap.mail.me.com'
        elif self.kind.lower() == "gmail":
            return 'imap.gmail.com'
    
    
    def login(self, username, password):
        self.M.login(username, password)
    
    
    def close(self):
        self.M.close()
        self.M.logout()


mb = None

def process(sentence):
    ''' Process the sentence '''
    global mb
    username = 'username'
    password = 'password'
    provider = 'provider'
    if not mb:
        mb = Mailbox(provider)
        mb.login(username, password)
    r = mb.get_unread()
    return r if r else ""



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