import time
import requests
import random

temp = [random.randint(20,40) for _ in range(10)]
humid = [random.randint(50,100) for _ in range(10)]
API_DELAY = 15

for t, h in zip(temp, humid):
    res = requests.get(f"https://api.thingspeak.com/update?api_key=3F387GR8DQHVRXGW&field1={t}&field2={h}")
    print(f"{time.asctime()} Response code {res.status_code} for t={t}, h={h}")
    time.sleep(API_DELAY)