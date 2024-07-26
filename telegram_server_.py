import socket
import threading
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from dotenv import load_dotenv
import os
import json

load_dotenv()
# Configuration
PORT = 8080
API_KEY = os.getenv("TELEGRAM_API")
HOST_UID_MAP = {}  # {uid: ip_address}
USER_UID_MAP = {}  # {telegram_id: uid}
HOST_UID_FILE = 'host_uid_map.json'
USER_UID_FILE = 'user_uid_map.json'

# Load data from JSON files
def load_data():
    global HOST_UID_MAP, USER_UID_MAP
    if os.path.exists(HOST_UID_FILE):
        with open(HOST_UID_FILE, 'r') as f:
            HOST_UID_MAP = json.load(f)
    if os.path.exists(USER_UID_FILE):
        with open(USER_UID_FILE, 'r') as f:
            USER_UID_MAP = json.load(f)

# Save data to JSON files
def save_data():
    with open(HOST_UID_FILE, 'w') as f:
        json.dump(HOST_UID_MAP, f, indent=4)
    with open(USER_UID_FILE, 'w') as f:
        json.dump(USER_UID_MAP, f, indent=4)

# Set up Telegram bot
application = Application.builder().token(API_KEY).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in USER_UID_MAP:
        await update.message.reply_text("Please send the UID displayed on the LCD.")
    else:
        uid = USER_UID_MAP[user_id]
        await update.message.reply_text(f"UID confirmed: {uid}")

async def set_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.args:
        uid = context.args[0]
        if uid in HOST_UID_MAP.values():
            USER_UID_MAP[user_id] = uid
            save_data()
            await update.message.reply_text(f"Your UID {uid} has been set.")
        else:
            await update.message.reply_text("Invalid UID. Please try again.")
    else:
        await update.message.reply_text("Please provide a UID.")

application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('setuid', set_uid))

# Server socket
def handle_client(client_socket):
    uid = str(len(HOST_UID_MAP) + 1)  # Example UID assignment
    HOST_UID_MAP[uid] = 'pending'  # Mark UID as pending
    client_socket.send(uid.encode('utf-8'))
    client_socket.close()
    save_data()

def server_thread():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', PORT))
    server.listen(5)
    print(f"Server listening on port {PORT}")

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"Connection from {addr}")
            handle_client(client_socket)
        except Exception as e:
            print(f"Error handling client: {e}")

# Start Telegram bot polling and server
if __name__ == '__main__':
    load_data()
    threading.Thread(target=server_thread, daemon=True).start()
    application.run_polling()