"""
Author: Andrew Higgins
https://github.com/speckly
Project Perishervation

Sensors utils
"""

import RPi.GPIO as GPIO
import time
import spidev
import Adafruit_DHT
from constants import TEMPHUMID_GPIO, BUZZER_GPIO, LDR_SPI_CHANNEL
import adxl345
from math import sqrt

ADDRESS=0x53

acc=adxl345.ADXL345(i2c_port=1,address=ADDRESS) #instantiate
acc.load_calib_value() #load calib. values in accel_calib
acc.set_data_rate(data_rate=adxl345.DataRate.R_100) #see datasheet
acc.set_range(g_range=adxl345.Range.G_16,full_res=True) # ..
acc.measure_start()

#acc.calibrate()

DHT = Adafruit_DHT.DHT11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_GPIO,GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0, 0)


# NOTE: This might be useless
def standardise(data: float, mn=0, mx=1023) -> float:
    if mn >= mx:
        raise ValueError("min must be less than max")
    return (data - mn) / (mx - mn)

def std_accel(raw: tuple) -> float:
    x, y, z = raw
    return sqrt(x**2 + y**2 + z**2)

def read_temphumid(gpio=None) -> tuple:
    return Adafruit_DHT.read_retry(DHT, TEMPHUMID_GPIO if gpio is None else gpio, 
        retries=5, delay_seconds=1)

def buzzer(beeps: int, duration: float) -> None:
    try:
        for i in range(beeps): # Number of beeps
            for state in [GPIO.HIGH, GPIO.LOW]:
                time.sleep(duration)
                GPIO.output(BUZZER_GPIO, state)
    except KeyboardInterrupt:
        GPIO.output(BUZZER_GPIO, GPIO.LOW)
        
def read_accel() -> tuple:
    return acc.get_3_axis_adjusted() # x, y, z

def read_light() -> int:
    # Black magic taken from the MCP3008 datasheet
    spi.max_speed_hz = 1350000
    r=spi.xfer2([1,8+LDR_SPI_CHANNEL<<4,0])
    data=((r[1]&3)<<8)+r[2]
    return data

    
