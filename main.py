from time import sleep
import sensors
import thingspeak
from constants import LIMITS, THINGSPEAK_API_DELAY

def check_limits(fields: list) -> None:
    # [temperature, humidity, shock, light]
    keys = ["temperature", "humidity", "acceleration", "light"]
    for key, magnitude in zip(keys, fields):
        field_limit = LIMITS.get(key)
        if field_limit is None:
            print("Your %s key is empty" % key)
            continue
        high_limit, low_limit = LIMITS[key].get("high"), LIMITS[key].get("low")
        if not all([magnitude < high_limit if high_limit else True, magnitude > low_limit if low_limit else True]):
            beeps, duration = LIMITS[key].get("beeps"), LIMITS[key].get("duration")
            if not all([beeps, duration]):
                print("Either beeps or duration is empty for %s, check it again" % key)
                continue
            sensors.buzzer(beeps=beeps, duration=duration)
        
cycle = 0

while True:
    cycle += 1 
    print("Cycle number: ", cycle) # NOTE: Might want to remove this
    temperature, humidity = sensors.read_temphumid() # deg or fah?, %
    acceleration = round(sensors.std_accel(sensors.read_accel()), 5) # 0 to 1
    light = sensors.read_light() # 0 to 1023
    field_list = [temperature, humidity, acceleration, light]
    
    #thingspeak.post(field_list) # uncomment when deploying
    
    #TODO: remove this when deploying
    if temperature is not None:
        print("tmp: ", temperature)
    if humidity is not None:
        print("hmd: ", humidity)
    if acceleration is not None:
        print("acc: ", acceleration)
    if light is not None:
        print("light: ", light)

    check_limits(field_list)
    
    sleep(THINGSPEAK_API_DELAY)
