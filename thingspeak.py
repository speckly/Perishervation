from constants import THINKSPEAK_API_DELAY
from dotenv import load_dotenv

THINGSPEAK_API_KEY = load_dotenv("TELEGRAM_API")

def ts_write(temperature: float = None, humidity: float = None, light: float)