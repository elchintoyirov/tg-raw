import requests
from config import BASE, TOKEN

offset = 0
while True:
    resp = requests.get(
        f"{BASE}{TOKEN}/getUpdates",
        params={
            "offset": offset,
            "timeout": 3,
        },
    ).json()

    for result in resp["result"]:
        offset = result["update_id"] + 1

        msg = result.get("message")
        if "text" in msg:
            text = msg["text"]
            chat_id = msg["chat"]["id"]
            requests.post(
                f"{BASE}{TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                },
            )
