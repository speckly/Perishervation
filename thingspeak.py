"""
Author: Andrew Higgins
https://github.com/speckly
Project Perishervation

TODO: Decide on which formatting method to use or create a separate env for rpi
"""

from dotenv import load_dotenv
from requests import get
from os import getenv

load_dotenv(".env")
TS_WRITE = getenv("TS_WRITE")

WRITE_BASE_URL = "https://api.thingspeak.com/update?api_key=%s" % TS_WRITE # why is rpi so outdated!!! TODO decide again

def post(thingspeak_fields: list) -> None:
	# MUST BE IN ORDER OF THE CHANNEL BELOW!!
	# https://thingspeak.com/channels/2597196/edit
	# [temperature, humidity, shock, light] 

	get_url = WRITE_BASE_URL
	for i, value in enumerate(thingspeak_fields, start=1):
		if value is not None:
			get_url += "&field%s=%s" % (i, value)
	
	res = get(get_url)
	if res.status_code != 200:
		print("Error uploading data to TS: %s" % res.text)
	
