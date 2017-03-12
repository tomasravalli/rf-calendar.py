# import BeautifulSoup library to scrap Federer's official website
from bs4 import BeautifulSoup
# import Twilio library to send SMS push notification
from twilio.rest import TwilioRestClient
import requests
import re

# open the txt file containing the updated list of tournaments
f = open("rf-tournaments.txt", "r+")
text = f.read()

# parse html from Federer's official website
url = 'http://www.rogerfederer.com/'
webpage = requests.get(url)
soup = BeautifulSoup(webpage.text, 'html.parser')

# set up SMS push notification
account_sid = 'AC66a5xxxxxxxxxxxxxxxxxx'
auth_token = '5d2414xxxxxxxxxxxxxxxxxxxxxx'
twilio_phone_number = '+15103986060'
my_phone_number = '+34xxxxxxxxx'


# create regex for the word 'miami'
free_regex = re.compile('miami')
# create list with all the alternatives
all_strings = list(soup.find_all("span", class_="ttourney"))
date = list(soup.find_all("span", class_="tmonth"))
# iterate through every class; if the class contains the word 'miami' we add it to an array "tournaments"
tournaments = [s.string for s in all_strings]


# if there is data on Federer's website, then the script runs
if tournaments:
# check for differences in the text
	if text != str(tournaments):
		f.write(str(tournaments))
		print("Update on Roger's calendar")
		body = 'Next tournaments:\n\n' + '\n'.join(tournaments)
		client = TwilioRestClient(account_sid, auth_token)
		client.messages.create(
			body=body,
			to=my_phone_number,
			From=twilio_phone_number
		)

f.close()
