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

# Global variables
FILENAME = "<FILEPATH_TO_YOUR_CLIPPINGS_FILE>"
SENDER_EMAIL = "<your_gmail_here>"
RECEIVER_EMAIL = "<your_recipient_email_here>"
PASSWORD = "<your_gmail_password_here>"
DATE = datetime.today().strftime("%m/%d/%Y")
NAME = "Blork McBlorkstein"
DICTIONARY_TXT = "./dictionary.txt" # Change this to your dictionary file!
APP_ID = "<YOUR_APP_ID_HERE>"
APP_KEY = "<YOUR_APP_KEY_HERE>"
LANGUAGE = "<YOUR_LANG_CODE_HERE for english = en-gb or en-us>"

def parse_kindle():
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
                a = line.translate(str.maketrans('', '', string.punctuation))
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
    if len(dict_words) >= 1:
        random_selector(phrases, dict_words)
    else:
        parse_kindle()


def random_selector(set_of_phrases, set_of_dict_words):
    # Get a random word and phrase of the day using numpy (np)
    phrase_rand = np.random.randint(0, (len(set_of_phrases)))
    word_rand = np.random.randint(0, (len(set_of_dict_words)))

    # save the phrases and dictionary words as lists
    p = list(set_of_phrases)
    q = list(set_of_dict_words)

    # Access the randomly chosen element from the lists
    phrase_send = p[phrase_rand]
    word_send = q[word_rand]

    dictionary_create(p, q, phrase_send, word_send)

def dictionary_create(list_of_phrases, list_of_words, phrase_send, word_send):
    tmp = set()

    # Open the specified "dictionary.txt" file
    with open(f"{DICTIONARY_TXT}", "r") as file:
        tmp = file.read().splitlines()

    # For each word in the list of dictionary words
    for word in list_of_words:
        # if the word is already in the list
        if word in tmp:
            # do nothing
            continue
        else:
            # otherwise add it to the temporary set
            tmp.append(word)

    # Dictionary.txt is now sorted!
    tmp = sorted(tmp)

    # Write this sorted dictionary to disk
    with open(f"{DICTIONARY_TXT}", "w") as f:
        for word in tmp:
            f.write("%s\n" % word)

    print(word_send)
    dictionary_call_email(word_send)

def dictionary_call_email(word='morass'):
    word_id = word.translate(str.maketrans('', '', string.punctuation))
    url = f"https://od-api.oxforddictionaries.com/api/v2/entries/{LANGUAGE}/{word_id.lower()}?fields=definitions%2Cetymologies%2Cexamples%2Cpronunciations&strictMatch=false"
    r = requests.get(url, headers={"Accept": "application/json", "app_id": APP_ID, "app_key": APP_KEY})
    results = r.json()
    # this pulls out the etymology from the json
    try:
        etymologies = results['results'][0]['lexicalEntries'][0]['entries'][0]['etymologies'][0]
        definition = results['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        category = results['results'][0]['lexicalEntries'][0]['lexicalCategory']['id']
        proper_def = '. '.join(i.capitalize() for i in definition.split('. '))
        audio_pronounce = results['results'][0]['lexicalEntries'][0]['pronunciations'][0]['audioFile']
        phonetic_sp = results['results'][0]['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling']
        code = "code {}\n".format(r.status_code)
        secondary_url = f"https://en.oxforddictionaries.com/definition/{word_id.lower()}"
        send_email(word, etymologies, definition, category, proper_def, audio_pronounce, phonetic_sp, code, secondary_url)
    except KeyError as ke:
        send_error_email(ke)

def send_error_email(error):
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Error e-mail: {DATE}"
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi {NAME},
    Error returned: {error}
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
          <h1>Hi {NAME}, serious problem here: {error}</h1>
          <h2>FIX IT NOW!!!</h2>
        </p>
      </body>
    </html>
    """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
    return 1

def send_email(word, etymologies, definition, category, proper_def, audio_pronounce, phonetic_sp, code, secondary_url):
    # Put in sender, recipient, login credentials
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Daily e-mail for {DATE}, word: {word}"
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi {NAME},
    Are you ready for a rad word of the day?
    Well, who cares, you're getting it anyway: {word}
    It means {proper_def}, comes from {etymologies}, and is pronounced {phonetic_sp}
    It sounds like {audio_pronounce}
    Find out more here: {secondary_url}!
    Also, Merriam Webster has a generic one!
    But ours is personalized... :-)
    Returned with {code}
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
          <h2>Are you ready for a rad word of the day?</h2>
          <h2>Well, who cares? You're getting it anyway: <b><i> {word} </b></i>, {category} </h2>
          <h2>It means: {proper_def}</h2>
          <h2>Here is where it comes from: {etymologies}</h2>
          <h2>{word} is pronounced: <b><i> {phonetic_sp} </b></i> </h2>
          <h2>It sounds like: {audio_pronounce} </h2>
          <h2>Find out more <a href={secondary_url}>here</a>!<h2>
          <h2>Also, <a href="https://www.merriam-webster.com/word-of-the-day">Merriam Webster</a> has a generic one!</h2>
          <h2>But ours is personalized... :-)</h2>
          <h2>For the nerds: returned with {code}...</h2>
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

    return 0

def main():
    parse_kindle()

if __name__ == '__main__':
    main()


"""

SOME OF MY MANY REFERENCES:

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
