import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

BASE = f"https://api.telegram.org/bot{TOKEN}"

resp = requests.get(f"{BASE}/getMe").json()
print(json.dumps(resp, indent=3))
