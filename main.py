import time
import requests
import random
import sensors
import thingspeak

API_DELAY = 15
cycle = 0

# for t, h in zip(temp, humid):
#     res = requests.get(f"https://api.thingspeak.com/update?api_key=3F387GR8DQHVRXGW&field1={t}&field2={h}")
#     print(f"{time.asctime()} Response code {res.status_code} for t={t}, h={h}")
#     time.sleep(API_DELAY)


while True:
    cycle += 1 
    print("Cycle number: ", cycle) # NOTE: Might want to remove this
    temperature, humidity = sensors.read_temphumid() # deg, %
    acceleration = round(sensors.std_accel(sensors.read_accel()), 5)
    light = sensors.read_light()
    
    #thingspeak.post(temperature, humidity, acceleration, light)
    
    #TODO: migrate this, this is temp
    if temperature is not None:
        print("tmp: ", temperature)
    if humidity is not None:
        print("hmd: ", humidity)
    if acceleration is not None:
        print("acc: ", acceleration)
    if light is not None:
        print("light: ", light)

    # TODO: Determine conditions for the buzzer to be sounded,
    if acceleration > 0.5:
        sensors.buzzer(beeps=2, duration=0.1)
    
    time.sleep(3)
