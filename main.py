import time
import requests
import random
import sensors

API_DELAY = 15

# for t, h in zip(temp, humid):
#     res = requests.get(f"https://api.thingspeak.com/update?api_key=3F387GR8DQHVRXGW&field1={t}&field2={h}")
#     print(f"{time.asctime()} Response code {res.status_code} for t={t}, h={h}")
#     time.sleep(API_DELAY)

while True:
    print(sensors.read_temphumid())
    
    time.sleep(API_DELAY)