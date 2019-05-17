#!/usr/bin/python

import csv
import email
import json
import numpy as np
import requests
import string
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Global variables - change these as things are moved around,
# to send e-mails to different people, etc.
FILENAME = "./clippings.txt"
SENDER_EMAIL = "<youremail@yourhoster.com>"
RECEIVER_EMAIL = "<recipient@test.com>"
PASSWORD = "<insert your gmail password here>"
DATE = datetime.today().strftime("%m/%d/%Y")
NAME = "<RECIPIENT>"
DICTIONARY_TXT = "./dictionary.txt"
APP_ID = "<oxford dictionary api app id>"
APP_KEY = "<oxford dictionary api app key>"
LANGUAGE = "en-us"

"""PARSING THE INPUT FILE (FILENAME)"""

# create sets that will contain the phrases and dictionary words
phrases = set()
dict_words = set()

# Open the file, readlines from it, etc.
with open(FILENAME, "r") as file:
    # define lines
    lines = file.readlines()
    for line in lines:
        # if line is just a new line or return
        if line.startswith("\n") or line.startswith("\r"):
            continue
        # if line is a word or phrase, they always start with alphabet, never with hyphen
        elif line != "" and line[0].isalpha():
            a = line.strip().lower()
            # https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
            a = line.translate(str.maketrans('', '', string.punctuation))
            # for some reason I had to strip it again
            b = a.strip().lower()
            # separate out words from phrases
            if ' ' in b:
                phrases.add(b)
            else:
                dict_words.add(b)
        elif line.startswith("=") or line.startswith("-"):
            continue
        else:
            continue

"""
RANDOM SELECTION OF A WORD
Here we use numpy to pick a random word and continue
saving the phrases and dictionary words as lists, etc.
"""


# You can also just use random.randint() if you import random
# This may be necessary if you can't get numpy functional in your
# python environment.
# Now use numpy to randomly generate a word + phrase of the day
# Get a random word and phrase of the day using numpy (np)
phrase_rand = np.random.randint(0, (len(phrases)))
word_rand = np.random.randint(0, (len(dict_words)))

# save the phrases and dictionary words as lists
p = list(phrases)
q = list(dict_words)

# Access the randomly chosen element from the lists
phrase_send = p[phrase_rand]
word_send = q[word_rand]

"""
CREATE A DICTIONARY TXT FILE:
Writing dictionary words to a text file,
but also checking if the words have been
in there before. This way I can create a
persistent text file on my computer, or
raspberry pi that will always hold all
of the dictionary files, regardless of the
status of the input file...
"""

# Create a new temporary list (each time)
tmp = set()

# Open the specified "dictionary.txt" file
with open(f"{DICTIONARY_TXT}", "r") as g:
    tmp = g.read().splitlines()

# For each word in the list of dictionary words
for word in dict_words:
    # if the word is already in the list
    if word in tmp:
        # do nothing
        continue
    else:
        # otherwise add it to the temporary list
        tmp.add(word)

# Dictionary.txt is now sorted!
tmp = sorted(tmp)

# Write this sorted dictionary to disk
with open(f"{DICTIONARY_TXT}", "w") as f:
    for word in tmp:
        f.write("%s\n" % word)


"""DICTIONARY PORTION
Here we use the Oxford Dictionaries API, special thanks
to their documention, to query their dictionary for our
target word - in this case a random word from our new
list of highlighted words!
"""

# change this to alter word/phrase
word_id = word_send

url = f"https://od-api.oxforddictionaries.com/api/v2/entries/{LANGUAGE}/{word_id.lower()}?fields=definitions%2Cetymologies%2Cexamples%2Cpronunciations&strictMatch=false"
r = requests.get(url, headers={"Accept": "application/json", "app_id": APP_ID, "app_key": APP_KEY})

# Basically creates a dictionary of lists, sets, and dictionaries
# from the json that the GET request returns
# This took a lot of my time, and didn't end up as complete
# as I would have hoped
results = r.json()

# this pulls out the etymology from the json
subset_r = results['results'][0]['lexicalEntries'][0]
a = str(subset_r['entries'][0]['etymologies'])
etymologies = str(a)

code = "code {}\n".format(r.status_code)

# Definition - need to finish
#b = results['results'][0]['lexicalEntries'][0]

"""EXPAND THIS SECTION - INCLUDE MORE SNIPPETS"""

# A little error feedback for the get request, if there is no error
# nothing will show up in the e-mail!
if not r:
    error_code = f"<h1>Ooopsies! We had an error {code}, try again!</h1>"
else:
    error_code = ""

# if this doesn't work try:
secondary_url = f"https://en.oxforddictionaries.com/definition/{word_id.lower()}"

# Not using this yet, but maybe will plugin phrase functionality later...
# startpage search query - no API key, etc. needed
phrase_url = f"https://www.startpage.com/do/dsearch?query={str(p[phrase_rand])}"

"""
E-MAIL PART:

So, in this part of the code, I use gmail to send an e-mail
in both plain text and html formats. Obviously here I am including
an e-mail address I specially made for this so that I don't have
to give my real gmail credentials. From realpython.com:
https://realpython.com/python-send-email/

"""
# Put in sender, recipient, login credentials

message = MIMEMultipart("alternative")
message["Subject"] = f"Daily e-mail for {DATE}, word: {word_send}"
message["From"] = SENDER_EMAIL
message["To"] = RECEIVER_EMAIL

# Create the plain-text and HTML version of your message
text = f"""\
Hi {NAME},
{error_code}
Are you ready for a rad word of the day?
Well, who cares, you're getting it anyway: {word_send}
Find out more here: {secondary_url}!
Also, Merriam Webster has a generic one!
But ours is personalized... :-)
"""

html = f"""\
<html>
  <body style="background-color:#7e987d;">
  <head>
        <meta charset="UTF-8">
        <meta content="width=device-width, initial-scale=1" name="viewport">
        <meta name="x-apple-disable-message-reformatting">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta content="telephone=no" name="format-detection">
        <title></title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet">
        <title>Webapp_Final</title>
  </head>
      <h1>Hi {NAME},</h1>
      {error_code}
      <h2>Are you ready for a rad word of the day?</h2>
      <h2>Well, who cares? You're getting it anyway: <b><i> {word_send} </b></i> </h2>
      <h2>Here is where it comes from: {etymologies}</h2>
      <h2>Find out more <a href={secondary_url}>here</a>!<h2>
      <h2>Also, <a href="https://www.merriam-webster.com/word-of-the-day">Merriam Webster</a> has a generic one!</h2>
      <h2>But ours is personalized... :-)</h2>
    </p>
  </body>
</html>
"""

# Now, send the e-mail
# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(SENDER_EMAIL, PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())


"""REFERENCES:
Here is where I found a great deal of code that helped me, especially in parsing the text file:

https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
https://stackoverflow.com/questions/17511270/how-can-i-add-items-to-an-empty-set-in-python
https://stackoverflow.com/questions/3301395/check-if-space-is-in-a-string
https://stackoverflow.com/questions/2395821/python-startswith-any-alpha-character
https://stackabuse.com/read-a-file-line-by-line-in-python/
https://www.vipinajayakumar.com/parsing-text-with-python/
https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.randint.html#numpy.random.randint
https://realpython.com/python-json/
https://www.scivision.dev/compile-install-python-beta-raspberry-pi/
https://askubuntu.com/questions/765494/how-to-install-numpy-for-python3
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

"""
