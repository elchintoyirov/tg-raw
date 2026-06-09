import requests
from pprint import pprint
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

    if not resp.get("ok"):
        pprint(resp)
        break

    for result in resp["result"]:
        offset = result["update_id"] + 1

        msg = result.get("message") or result.get("edited_message")
        if not msg or "text" not in msg:
            continue

        chat_id = msg["chat"]["id"]
        user_text = msg["text"]
        is_edit = "edited_message" in result

        if is_edit is True:
            text = f"Edit: {before_edit} -> {user_text}"
        else:
            text = f"Message: {user_text}!"
            before_edit = user_text

        requests.post(
            f"{BASE}{TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
        )
