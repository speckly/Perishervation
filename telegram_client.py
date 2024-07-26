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

# Send UID to Telegram bot for confirmation
def send_uid_to_bot(uid):
    # Replace with your Telegram chat ID or get it dynamically if needed
    chat_id = 'YOUR_TELEGRAM_CHAT_ID'
    response = requests.post(
        f"{TELEGRAM_API_URL}sendMessage",
        params={
            'chat_id': chat_id,
            'text': f"Please confirm this UID: {uid} by sending /setuid {uid}"
        }
    )
    if response.status_code == 200:
        print("UID sent to Telegram bot successfully.")
    else:
        print(f"Failed to send UID to Telegram bot. Status code: {response.status_code}, response: {response.text}")

def main():
    # Get UID from the server
    uid = get_uid()
    print(f"Received UID: {uid}")
    
    # Send UID to Telegram bot
    # send_uid_to_bot(uid)

if __name__ == '__main__':
    main()
