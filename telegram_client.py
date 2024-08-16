"""
Author: Andrew Higgins
https://github.com/speckly
Project Perishervation

Not to be deployed, only simulates
send_alert and get_uid are deployed
"""

import socket
# import requests
from constants import TELEGRAM_SERVER_IP
from dotenv import load_dotenv
import os

load_dotenv()
# Configuration
SERVER_PORT = 8080
MY_PORT = 8081
API_KEY = os.getenv("TELEGRAM_API")
TELEGRAM_API_URL = f'https://api.telegram.org/bot{API_KEY}/'

# Connect to the server and get UID
def get_uid():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((TELEGRAM_SERVER_IP, SERVER_PORT))
        except ConnectionRefusedError:
            return "Telegram server down"
        client.sendall("uid".encode('utf-8'))
        uid = client.recv(1024).decode('utf-8')
        return uid

def send_alert(data: list) -> None:
    # [temperature, humidity, shock, light]
    body = ""
    fields = ["temperature", "humidity", "shock", "light"]
    body = ",".join("{}:{}".format(field, magnitude) for magnitude, field in zip(data, fields) if magnitude) # cant use f string in rpi???????
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((TELEGRAM_SERVER_IP, SERVER_PORT))
        client.sendall(body.encode('utf-8'))
        # response = client.recv(1024).decode('utf-8')
        # print(f"Server response: {response}")

def main():
    uid = get_uid()
    print(f"Received UID: {uid}")

if __name__ == '__main__':
    main()
