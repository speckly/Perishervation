"""
Author: Andrew Higgins
https://github.com/speckly
Project Perishervation

This file contains all the constants used in Perishervation
These constants may be modified due to changing needs.
It is recommended that you understand the usage of the constant before making any changes"""

THINGSPEAK_API_DELAY = 2 # Delay in seconds between dataset pushes to the Thingspeak channel
TEMPHUMID_GPIO = 21 # DHT22 Temp and Humid
LDR_SPI_CHANNEL = 0
BUZZER_GPIO = 18
CALIB_FILE = 'accel_calib.txt'

# high: highest magnitude a variable can go before the buzzer is sounded
# low: same
# TODO: Determine conditions for the buzzer to be sounded, is temperature in fahrenheit lmao
LIMITS = {
	"temperature": {"high": 120, "low": 32, "beeps": 2, "duration": 0.1},
	"humidity": {"high": 50, "beeps": 1, "duration": 0.1},
	"acceleration": {"high": 0.5, "beeps": 3, "duration": 0.1},
	"light": {"low": 300, "beeps": 2, "duration": 0.2}
}

TELEGRAM_SERVER_IP = "172.23.37.96"
	
