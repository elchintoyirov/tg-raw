import html
import requests
from config import BASE, TOKEN


def send(chat_id, text, **extra):
    requests.post(
        f"{BASE}{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            **extra,
        },
    )


offset = 0
while True:
    resp = requests.get(
        f"{BASE}{TOKEN}/getUpdates",
        params={"offset": offset, "timeout": 3},
    ).json()

    for result in resp["result"]:
        offset = result["update_id"] + 1

        msg = result.get("message")
        if not msg or "text" not in msg:
            continue

        chat_id = msg["chat"]["id"]
        user_text = msg["text"]

        if user_text == "/html":
            send(
                chat_id,
                "<b>bold</b>, <i>italic</i>, <u>underline</u>, "
                '<a href="https://telegram.org">link</a>',
                parse_mode="HTML",
            )

        elif user_text == "/md":
            send(chat_id, "*bold* and _italic_", parse_mode="MarkdownV2")

        elif user_text == "/entities":
            send(
                chat_id,
                "Hello world",
                entities=[{"type": "bold", "offset": 6, "length": 5}],
            )

        else:
            safe = html.escape(user_text)
            send(chat_id, f"You said: <b>{safe}</b>", parse_mode="HTML")
