import socket
import requests
from constants import TELEGRAM_SERVER_IP
from dotenv import load_dotenv
import os

load_dotenv()
# Configuration
PORT = 8080
API_KEY = os.getenv("TELEGRAM_API")
TELEGRAM_API_URL = f'https://api.telegram.org/bot{API_KEY}/'

# Connect to the server and get UID
def get_uid():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((TELEGRAM_SERVER_IP, PORT))
        uid = client.recv(1024).decode('utf-8')
        return uid

def main():
    uid = get_uid()
    print(f"Received UID: {uid}")

if __name__ == '__main__':
    main()
