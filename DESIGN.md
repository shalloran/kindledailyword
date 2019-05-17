# SMH CS50 FINAL PROJECT DESIGN.md

# Final Project CS50 Spring 2019
## Customized word of the day e-mail

This project was technically constructed using a lot of the tools that CS50 provided me. As someone who had no experience whatsoever in programming, this was a huge step for me - and honestly I couldn't have conceived of how to do this before this class. Because I was simultaneously taking an Intro to Python class, this is all written in python. The idea for this project came about when I was thinking about how the kindle (ebook reader) I use actually grabs content once you highlight it. After a few months of programming under my belt, I thought how hard could this be - to recreate how they pull data from a dictionary stored on the device, parse it, and present it to the user. That is when I stumbled across the "myclippings.txt" file stored on my kindle - and started to poke around.

After realizing that I wanted to establish persistence - that is continue to get these e-mails despite not having opened my computer, I realized it was raspberry pi time. So, a lot of the design went into making this a standalone app that I could install on my raspberry pi 3+ which, when running Raspbian (Debian based operating system specifically designed for the pi), already has python installed on it! Unfortunately, it was python 3.5 - which I didn't realize until it was too late does not support the new "f-strings" that python 3.7+ does. This is integral for my project because the html gets sent via a string over e-mail - which means that using f-strings enabled me to insert variables - much like we did with webapps. This way, I could create a custom e-mail like below:

Hi {NAME}, ... word of the day is {word_of_the_day}... and so on.

So, I had to quickly figure out how to upgrade my pi's python! All of this is to say - I wanted something light that I could send over a headless connection to a raspberry pi. This is not a fancy program, but I was so elated that I was able to get this to work, and am impressed by how much I have learned over the course of this semester!

Thanks everyone, especially my TA (Josh), and my awesome section!

Best,
Sean
