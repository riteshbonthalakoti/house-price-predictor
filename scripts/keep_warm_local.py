import time
import requests
import datetime

url = "https://house-price-predictor-api-lq99.onrender.com/health"
print(f"Starting local keep-warm daemon for Render backend: {url}")

while True:
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res = requests.get(url, timeout=15)
        print(f"[{now}] Keep-Alive Status: {res.status_code} | Response: {res.text.strip()}")
    except Exception as e:
        print(f"[{now}] Keep-Alive Warning: {e}")
    time.sleep(180)  # Pings every 3 minutes to keep Render awake
