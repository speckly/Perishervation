# TODO: Decide on which formatting method to use or create a separate env for rpi

from constants import THINKSPEAK_API_DELAY
from dotenv import load_dotenv

TS_READ = load_dotenv("TS_READ")
TS_WRITE = load_dotenv("TS_WRITE")

WRITE_BASE_URL = "https://api.thingspeak.com/update?api_key=%s" % TS_WRITE # why is rpi so outdated!!! TODO decide again

def post(temperature: float = None, humidity: float = None, shock: float = None, light: float = None):
	# MUST BE IN ORDER OF THE CHANNEL BELOW!!
    # https://thingspeak.com/channels/2597196/edit
    
    # remember to process with standardisation
	thingspeak_fields = [temperature, humidity, shock, light]
	post_url = WRITE_BASE_URL
	for i, value in enumerate(thingspeak_fields, start=1):
		if value is not None:
			post_url += "&field%s=%s" % (i, value)
	print(post_url)
