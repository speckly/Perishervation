"""
Author: Andrew Higgins
https://github.com/speckly
Project Perishervation

This will be deployed on a central server responsible for the Telegram networking in Perishervation
"""

import socket
import threading
import requests
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from dotenv import load_dotenv
import os
import json
from collections import defaultdict

class UIDGenerator:
    def __init__(self):
        self.counter = defaultdict(int)
    
    def get_uid(self, key):
        self.counter[key] += 1
        return self.counter[key]

load_dotenv()
API_KEY = os.getenv("TELEGRAM_API")
if not API_KEY:
    print('No .env file or Telegram API Key? Create one according to README.md')
    exit(1)

PORT = 8080
CLIENT_PORT = 8082
HOST_UID_MAP = {'free': 1, 'hosts': {}}  # {uid: ip_address}
USER_UID_MAP = {}  # {telegram_id: uid}
HOST_UID_FILE = 'host_uid_map.json'
USER_UID_FILE = 'user_uid_map.json'

def load_data():
    global HOST_UID_MAP, USER_UID_MAP

    if os.path.exists(HOST_UID_FILE):
        try:
            with open(HOST_UID_FILE, 'r') as f:
                HOST_UID_MAP = json.load(f)
        except json.decoder.JSONDecodeError:
            print("Resetting host uid file")
            with open(HOST_UID_FILE, 'w') as f:
                json.dump({'free': 1, 'hosts': {}}, f, indent=4)

    if os.path.exists(USER_UID_FILE):
        try:
            with open(USER_UID_FILE, 'r') as f:
                USER_UID_MAP = json.load(f)
        except json.decoder.JSONDecodeError:
            print("Resetting user uid file")
            with open(USER_UID_FILE, 'w') as f:
                json.dump({}, f, indent=4)

def save_data():
    with open(HOST_UID_FILE, 'w') as f:
        json.dump(HOST_UID_MAP, f, indent=4)
    with open(USER_UID_FILE, 'w') as f:
        json.dump(USER_UID_MAP, f, indent=4)

application = Application.builder().token(API_KEY).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in USER_UID_MAP.values():
        await update.message.reply_text("Set the UID displayed on https://perishervation.com/get_uid using /setuid <uid>")
    else:
        for addr in USER_UID_MAP:
            if USER_UID_MAP[addr] == user_id:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    try:
                        client.connect((addr, CLIENT_PORT))
                        client.sendall("OK".encode('utf-8'))
                    except ConnectionRefusedError:
                        # print(f"{addr}, connection refused consider blacklisting") # reduce server resources or possible cyberattacks
                        await update.message.reply_text(f"Client may be down, check it")
                        return
                await update.message.reply_text(f"Good to go")
                break

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in USER_UID_MAP.values():
        await update.message.reply_text("Set the UID displayed on https://perishervation.com/get_uid using /setuid <uid>")
    else:
        for addr in USER_UID_MAP:
            if USER_UID_MAP[addr] == user_id:
                await update.message.reply_text(f"Stopped")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.connect((addr, CLIENT_PORT))
                    client.sendall("STOP".encode('utf-8'))
                break

async def set_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_uid = update.message.from_user.id
    if context.args:
        rpi_uid = context.args[0]
        if rpi_uid.isdigit() and int(rpi_uid) in HOST_UID_MAP['hosts'].values():
            rpi_uid = int(rpi_uid)
            for addr in HOST_UID_MAP['hosts']:
                if HOST_UID_MAP['hosts'][addr] == rpi_uid:
                    USER_UID_MAP[addr] = telegram_uid
                    save_data()
                    await update.message.reply_text(f"Your rpi_uid {rpi_uid} has been set.")
            return
        await update.message.reply_text("Invalid rpi_uid. Please try again.")
    else:
        await update.message.reply_text("Please provide a rpi_uid.")

def handle_client(client_socket, address):
    message = client_socket.recv(1024).decode('utf-8')
    
    if message == "uid":
        if address not in HOST_UID_MAP['hosts']:
            uid = HOST_UID_MAP['free']
            HOST_UID_MAP['hosts'][address] = uid
            HOST_UID_MAP['free'] += 1
        else:
            uid = HOST_UID_MAP['hosts'][address]
            
        save_data()
        client_socket.sendall(str(uid).encode('utf-8'))
    else: # send alert data to client
        output = ["High variable warning:"]
        for pair in message.split(","):
            field, magnitude = pair.split(":")
            if magnitude and field in ["temperature", "humidity", "shock", "light"]:
                output.append(f"{field.capitalize()}: {magnitude}")
        requests.get(f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={USER_UID_MAP[address]}&text={'\n'.join(output)}")

    client_socket.close()

def server_thread():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', PORT))
    server.listen(5)
    print(f"Server listening on port {PORT}")

    while True:
        try:
            client_socket, addr = server.accept()
            handle_client(client_socket, addr[0])
        except Exception as e:
            print(f"Error handling client: {e}")

# Start Telegram bot polling and server
if __name__ == '__main__':
    load_data()
    threading.Thread(target=server_thread, daemon=True).start()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('setuid', set_uid))
    application.add_handler(CommandHandler('stop', stop))
    application.run_polling()