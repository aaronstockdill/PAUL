## Flags for the system. TRY TO AVOID TOUCHING.
#  VERSION is the version number of the Paul installation.
#  VERBOSE is for debug info.
#  NOISY for Paul to talk.
#  MAX_LOG_SIZE is the maximum number of lines allowed in the log file.
#  LOGGING determines if Paul will write the log to the file.
#  USER is the current user profile to use.
#  SKIP_LOGIN is set to the name to default to, or False.
#  IT is whatever 'it' could be, changes automatically.
#  SEND is the function that is used to send data to the user.
#  GET is the function that is used to get data from the user.
#  EXEC is the function that is used to send executable scripts to the user.

flags = {
    "VERSION": "0.3.2",
    "VERBOSE": True,
    "NOISY": False,
    "MAX_LOG_SIZE": "500",
    "LOGGING": True,
    "USER": None,
    "SKIP_LOGIN": False,
    "IT": None,
    "SEND": None,
    "GET": None,
    "EXEC": None,
}

# Add users with profiles here. At the moment, this is a manual process.
# Create a new file for each user called "name.py", replacing name with the 
# name used here. Just copy the contents of default into the file, then change
# as necessary.

users = {
    "default",
}