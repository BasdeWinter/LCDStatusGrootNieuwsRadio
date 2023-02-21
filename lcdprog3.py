#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import json
import subprocess
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from RPLCD import CharLCD
GPIO.setwarnings(False)
lcd_cols = 20
lcd_rows = 4
status = 0

lcd = CharLCD(cols=lcd_cols, rows=lcd_rows, pin_rs=4, pin_e=17, pins_data=[18, 23, 27, 22], numbering_mode=GPIO.BCM)
lcd.clear()

chromedriver = "/usr/lib/chromium-browser/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-sh-usage")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
    
def write_to_lcd(lcd, framebuffer, num_cols):
    #Write the frambuffer to specified LCD
    lcd.home()
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string("\r\n")
 
def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.2):
    padding = ' ' * num_cols
    s = padding + string + padding
    for i in range(len(s) - num_cols + 1):
        framebuffer[row] = s[i:i+num_cols]
        write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)
    framebuffer[row] = string
    write_to_lcd(lcd, framebuffer, num_cols)

def scroll_if_needed(lcd, framebuffer, num_cols):
    for row in framebuffer:
        if len(row) > num_cols:
            loop_string(row, lcd, framebuffer, framebuffer.index(row), num_cols)
             
def get_volumio_track_name():
	status = get_volumio_status()
	if (status):
		if (len(status["title"].split(" - ")) > 0):
			return status["title"].split(" - ")[0]			  
		else:			
			return "Tijd: %s" %time.strftime("%H:%M") 
	else: 		  
		return "Tijd: %s" %time.strftime("%H:%M") 

def get_volumio_artist_name():
	status = get_volumio_status()
	if (status):
		if (len(status["title"].split(" - ") ) == 2):			
			return status["title"].split(" - ")[1]
		else:
			return "Datum: %s" %time.strftime("%d/%m/%Y")
	else:
		return "Datum: %s" %time.strftime("%d/%m/%Y")
	
def get_volumio_status():
	#set the value of status to the output of the volumio status command
	output = subprocess.run("/usr/local/bin/volumio status", capture_output=True, shell=True, text=True)
	if(output.stderr != ""):
		return False
	else:
		status = json.loads(output.stdout)
		return status

while True:
	content = ""
	try:
		driver.get("https://player.grootnieuwsradio.nl/")
		#give enough time for the song request to be completed and rendered by javascript
		time.sleep(6)
		content = driver.page_source
	except:
		#an exception occurred with selenium, try again in 30sec
		time.sleep(30)

	soup = BeautifulSoup(content, "html.parser")

	show_name = soup.find("div", class_="show__info__name")
	show_time = soup.find("div", class_="show__info__time")
	show_host = soup.find("div", class_="show__info__host-name")
	track_name = soup.find("div", class_="player-metadata__track__track-name")
	artist_name = soup.find("div", class_="player-metadata__track__artist-name")

	framebuffer = [
		"*PROGRAMMA*",
		"*PROGRAMMAMAKER*",
		"Tijd: %s" %time.strftime("%H:%M"),
		"Datum: %s" %time.strftime("%d/%m/%Y")
	]

	if hasattr(show_name, "text"):
		framebuffer[0] = show_name.text.strip()
	if hasattr(show_time, "text"):
		framebuffer[0] = framebuffer[0] + " - " + show_time.text.split("-")[0].strip() + "-" + show_time.text.split("-")[1].strip()
	if hasattr(show_host, "text"):
		framebuffer[1] = show_host.text.strip()
	if hasattr(track_name, "text"):
		framebuffer[2] = track_name.text.strip()
	else:
		framebuffer[2] = get_volumio_track_name()    
	if hasattr(artist_name, "text"):
		framebuffer[3] = artist_name.text.strip()
	else:
		framebuffer[3] = get_volumio_artist_name()

	write_to_lcd(lcd, framebuffer, lcd_cols)

	scroll_if_needed(lcd, framebuffer, lcd_cols)
