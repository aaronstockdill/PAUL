'''
new_user.py
Create a new user for Paul to access.
Author: Aaron Stockdill
'''

import shutil

import paul

def edit_file(name):
    ''' Bring the basic user data up to date. '''
    info = {
        "username": name.lower(),
        "name": name.title(),
        "first_run": "True"
    }
    
    title = paul.interact("Ok, {}, quick few questions".format(name.title()) 
                        + "\nWhat would you like "
                        + "me to use as a title?\nFor example, sir, ma'am...",
                        response="arb")
    temp = paul.interact("Fantastic. Now, do you prefer to use Fahrenheit "
                  + "or Celcius?",
                  response="arb")
    city = paul.interact("Awesome. And lastly, where do you live, "
                  + "{}?".format(name.title()),
                  response="arb")
    city.replace(" ", "%20").replace("'", "%27").replace("-", "%2D")
    url = ("http://query.yahooapis.com/v1/public/yql?q=select%20*%20from" 
         + "%20geo.places%20where%20text%3D%22{}%22&format=xml".format(city))
    
    dom = paul.DOM.fromURL(url)
    woeid = dom["woeid"][0][0]
    
    info["title"] = title
    info["temp"] = temp[0].upper()
    info["woeid"] = woeid
    
    for key, val in info.items():
        settings_file = "PAUL/Settings/{}.py".format(name.lower())
        sub = "    \"{}\": \"{}\",\n".format(key, val)
    
        lines = open(settings_file).readlines()
        for i, line in enumerate(lines):
            if line.startswith("    \"" + key + "\""):
                lines[i] = sub
                open(settings_file, "w").write("".join(lines))



def add_to_system(name):
    ''' Add the name to the system file, as one of the users. '''
    filename = "PAUL/Settings/system.py"
    
    file = open(filename, "r")
    lines = file.readlines()[:-1]
    file.close()
    
    lines.append('    "{}",\n'.format(name.lower()))
    lines.append("}\n")
    
    file = open(filename, "w")
    file.write("".join(lines))
    file.close()



def main(name):
    ''' Create a new account for the user based on the name provided,
        and further questions. '''
    
    paul.interact("Hi there, {}!\n".format(name.title()) + 
                  "I'm just creating you an account now.")
    shutil.copyfile("PAUL/Settings/default.py",
                    "PAUL/Settings/{}.py".format(name.lower()))
    add_to_system(name)
    edit_file(name)
    paul.interact("Ok, that should all be set up for you now!")