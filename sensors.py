import RPi.GPIO
import Adafruit_DHT
from constants import ACCEL_SCL, ACCEL_SDA, TEMPHUMID_GPIO

DHT = Adafruit_DHT.DHT11

def standardise(data: float, mn=0, mx=1023) -> float:
    if mn >= mx:
        raise ValueError("min must be less than max")
    return (data - mn) / (mx - mn)

def read_temphumid(gpio=None) -> tuple:
    return Adafruit_DHT.read_retry(DHT, TEMPHUMID_GPIO if gpio is None else gpio)
