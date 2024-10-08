from flask import Flask
from flask import render_template
from telegram_client import get_uid
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    uid = get_uid()
    data = requests.get(f"https://api.thingspeak.com/channels/2597196/feeds.json?").json()

    return render_template("index.html", value=uid, thingspeak_data = data)

def main():
    app.run(port=5050)

if __name__ == "__main__":
    main()