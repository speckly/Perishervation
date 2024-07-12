import requests
import dotenv
from PIL import Image
from io import BytesIO

hardcode = dotenv.get_key(".env", "TELEGRAM_API")
h2 = "800759626"
# r = requests.get(f"https://api.telegram.org/bot{hardcode}/getUpdates")
# print(r.json())

img = Image.open("test.jpg")
image_stream = BytesIO()
img.save(image_stream, format="JPEG")
image_stream.seek(0)

# message = string.digits
# r = requests.get(f"https://api.telegram.org/bot{hardcode}/sendMessage?chat_id={h2}&text={message}")

url = f"https://api.telegram.org/bot{hardcode}/sendPhoto"
files = {'photo': ('image.jpg', image_stream)}
data = {'chat_id': h2}
print(requests.post(url, files=files, data=data).json())