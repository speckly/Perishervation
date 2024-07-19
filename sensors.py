import RPi.GPIO as GPIO
import time
import spidev
import Adafruit_DHT
from constants import ACCEL_SCL, ACCEL_SDA, TEMPHUMID_GPIO, BUZZER_GPIO, LDR_SPI_CHANNEL

DHT = Adafruit_DHT.DHT11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_GPIO,GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0, 0)

#accelerometer = adafruit_adxl34x.ADXL345(i2c)

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
        
def read_accel():
    pass

def read_light() -> int:
    # Black magic taken from the MCP3008 datasheet
    spi.max_speed_hz = 1350000
    r=spi.xfer2([1,8+LDR_SPI_CHANNEL<<4,0])
    data=((r[1]&3)<<8)+r[2]
    return data

    
