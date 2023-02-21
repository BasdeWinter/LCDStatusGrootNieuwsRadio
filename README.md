# LCDStatusGrootNieuwsRadio
Python script that Scrapes the Groot Nieuws Radio player to show the stats on a local LCD display connected to a RPI via GPIO

Falls back on "volumio status" for track and artist name if not available on the web. Sometimes it is available on the web and sometimes in the JSON returned by "volumio status" (for some reason) so this way it is most redundant. 

Uses the Dutch language but this can be changed easily

requires:

sudo apt-get install python3-RPI.GPIO

sudo apt-get install python3-bs4

sudo pip install RPLCD

(/usr/bin/python3 -m pip install RPLCD)

sudo apt-get install python3-selenium

sudo apt-get install chromium-driver


Credits: 
RPLCD - https://rplcd.readthedocs.io/en/stable/index.html
Danilo Bargen - https://blog.dbrgn.ch/2014/4/20/scrolling-text-with-rplcd/
