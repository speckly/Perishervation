from flask import Flask
from flask import render_template
from telegram_client import get_uid
# from telegram_server_ import UIDGenerator
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    # uid_class = UIDGenerator()
    # uid = uid_class.get_uid()
    uid = 1
    data = requests.get(f"https://api.thingspeak.com/channels/2597196/feeds.json?").json()
   

    return render_template("index.html", value=uid, thingspeak_data = data)

if __name__ == "__main__":
    app.run(debug=True)