import RPi.GPIO
import Adafruit_DHT
from constants import ACCEL_SCL, ACCEL_SDA, TEMPHUMID_GPIO

DHT = Adafruit_DHT.AM2302

def standardise(data: float, mn=0, mx=1023) -> float:
    if mn >= mx:
        raise ValueError("min must be less than max")
    return (data - mn) / (mx - mn)

def read_temphumid() -> tuple[float, float]:
    return Adafruit_DHT.read_retry(DHT, TEMPHUMID_GPIO)
