import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from constants import ACCEL_SCL, ACCEL_SDA, TEMPHUMID_GPIO, BUZZER_GPIO

DHT = Adafruit_DHT.DHT11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_GPIO,GPIO.OUT) 

def standardise(data: float, mn=0, mx=1023) -> float:
    if mn >= mx:
        raise ValueError("min must be less than max")
    return (data - mn) / (mx - mn)

def read_temphumid(gpio=None) -> tuple:
    return Adafruit_DHT.read_retry(DHT, TEMPHUMID_GPIO if gpio is None else gpio, 
        retries=5, delay_seconds=1)

def buzzer() -> None:
    try:
        for i in range(3): # Number of beeps
            for state in [GPIO.HIGH, GPIO.LOW]:
                time.sleep(0.2)
                GPIO.output(BUZZER_GPIO, state)
    except KeyboardInterrupt:
        GPIO.output(BUZZER_GPIO, GPIO.LOW)
