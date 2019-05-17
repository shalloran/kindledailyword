# SMH CS50 FINAL PROJECT README.MD

# Sean Halloran Final Project CS50 Spring 2019
## Customized word of the day e-mail

This application, found in the python file called application.py, is intended to help the user import a text file, called myclippings.txt (in kindle format) of highlighted words and phrases taken during their own reading. This application will then parse that file, output a dictionary file (if not the first time, add to dictionary file), and return a random word from this dictionary of words. This random word will get included in a GET request to the Oxford Dictionaries API which will be used to pull data about the word's origin, and a link to the Oxford page for that word entry. This application then sends the user a customized e-mail with all of this information about a randomly chosen word every day.

Use case:

If you have been using a kindle for years, you will have a massive text file of highlighted words or passages - that no one will ever read through, nevermind do anything with! This program is to help you improve your vocabulary by reinforcing that word that you learned while reading on a different day. Primarily, the Oxford Dictionaries API is used here, as well as gmail's ability to send e-mails through python. This is a very simple program that will give you daily gifts if you so choose!

Instructions:

Using the CS50 IDE, you can just execute this python file by typing python application.py in the directory. If the clippings file has been named properly, and the you have created an empty dictionary.txt file and appropriately adjusted the global variables at the top of the file, you should have no problems. Double check your file paths and any of the information contained here, like passwords, recipients e-mail address, etc. Because of these variables being at the top, you shouldn't have to change any code in the following lines if you keep the variable names the same.

Once you have run the file - you should see the dictionary.txt file populated with (in this case) 376 entries. The clippings.txt file should be unaltered, and there should now be a new e-mail in the inbox you have specified! Voila!

Raspberry Pi 3B+ Implementation:

For my implementation of this project, I actually moved the python file, dictionary file, and clippings files to my Raspberry Pi 3B+ because this is the only computer at home I always have running - doing some home automation stuff. Since I figured this was already running Python 3.5, I will have no issues, right? Wrong. I had to upgrade the raspberry pi to python 3.8, because evidently f-strings are not supported pre 3.7. As discussed in the Design.md, this is an important consideration. So here are a few tips if you are trying to run this the same way:

1. Go here: https://www.scivision.dev/compile-install-python-beta-raspberry-pi/
2. After you've done all of that, read the python documentation about how to set up virtual environments, here: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
3. Beat your head against a wall because numpy isn't supported. Try to install numpy 8 times.
4. Make sure all of the links are correct - under global variables section at top of application.py
