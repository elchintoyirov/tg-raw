import requests
from pprint import pprint
from config import BASE, TOKEN


def send_menu(chat_id: int):
    requests.post(
        f"{BASE}{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": "Tap the button to fire a callback_query: ",
            "reply_markup": {
                "inline_keyboard": [[{"text": "Press me", "callback_data": "btn:1"}]]
            },
        },
    )


def main():
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

            if "callback_query" in result:
                requests.post(
                    f"{BASE}{TOKEN}/answerCallbackQuery",
                    json={
                        "callback_query_id": result["callback_query"]["id"],
                        "text": "Got it",
                    },
                )

            msg = result.get("message") or result.get("edited_message")
            if not msg or "text" not in msg:
                continue

            chat_id = msg["chat"]["id"]
            user_text = msg["text"]
            is_edit = "edited_message" in result

            if is_edit is True:
                text = f"Edit: {before_edit} -> {user_text}"
            elif user_text == "/menu":
                send_menu(chat_id)
                continue
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


if __name__ == "__main__":
    main()
