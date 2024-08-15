"""
Author: Andrew Higgins
https://github.com/speckly
Project Perishervation
"""

import threading
import random
import socket
from time import sleep
import thingspeak
import telegram_client
from constants import LIMITS, GLOBAL_DELAY, SIMULATION, CLIENT_PORT
import app
if not SIMULATION:
    import sensors

CLIENT_PORT = 8082
alert_telegram = False # determines if the RPI should send alerts to telegram server at runtime

def listen_response():
    global alert_telegram

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', CLIENT_PORT))
    server.listen(5)
    while True:
        try:
            client_socket, addr = server.accept()
            message = client_socket.recv(1024).decode('utf-8')
            alert_telegram = message == "OK"
        except Exception as e:
            print(f"Error handling client: {e}")

def check_limits(fields: list) -> list:
    keys = ["temperature", "humidity", "acceleration", "light"]
    hits = []
    for key, magnitude in zip(keys, fields):
        field_limit = LIMITS.get(key)
        if field_limit is None:
            # print("Your %s key is empty" % key)
            continue
        high_limit, low_limit = LIMITS[key].get("high"), LIMITS[key].get("low")
        if not all([magnitude < high_limit if high_limit else True, magnitude > low_limit if low_limit else True]):
            beeps, duration = LIMITS[key].get("beeps"), LIMITS[key].get("duration")
            if not all([beeps, duration]):
                print("Either beeps or duration is empty for %s, check it again" % key)
                continue
            if not SIMULATION:
                sensors.buzzer(beeps=beeps, duration=duration)
            hits.append(magnitude)
        else:
            hits.append(None)
    return hits

def main_loop():
    cycle = 0
    empty_hits = [None] * 4

    while True:
        cycle += 1 
        print("Cycle number: ", cycle) # NOTE: Might want to remove this
        if SIMULATION:
            field_list = [random.randint(40,125), random.randint(20,90), round(random.random(), 5), random.randint(280,500)]
        else:
            temperature, humidity = sensors.read_temphumid() # deg or fah?, %
            acceleration: float = round(sensors.std_accel(sensors.read_accel()), 5) # 0 to 1
            light: int = sensors.read_light() # 0 to 1023
            field_list = [temperature, humidity, acceleration, light]
        
        #thingspeak.post(field_list) # TODO: uncomment when deploying
        
        #TODO: remove this when deploying [temperature, humidity, shock, light]
        print(field_list, alert_telegram)

        hits: list = check_limits(field_list)
        if alert_telegram and hits != empty_hits:
            telegram_client.send_alert(hits)
        
        sleep(GLOBAL_DELAY)

if __name__ == "__main__": # dont set daemon, nah dont
    threading.Thread(target=listen_response).start()
    threading.Thread(target=main_loop).start()
    app.main() # Blocking
    # app.app.run(port=5050)