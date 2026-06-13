import requests

from config import BASE, TOKEN


class TelegramBot:
    def __init__(self, token, base_url):
        self.token = token
        self.base_url = f"{base_url}{token}"
        self.offset = 0
        self.media_groups: dict = {}

    def get_updates(self, timeout=3):
        url = f"{self.base_url}/getUpdates"
        params = {"offset": self.offset, "timeout": timeout}
        try:
            response = requests.get(url, params=params).json()
            return response.get("result", [])
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return []

    def send_message(self, chat_id, text):
        url = f"{self.base_url}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text})

    def send_photo(self, chat_id, photo_data, caption=""):
        url = f"{self.base_url}/sendPhoto"
        requests.post(
            url, json={"chat_id": chat_id, "photo": photo_data, "caption": caption}
        )

    def send_document(self, chat_id, document_data, caption=""):
        url = f"{self.base_url}/sendDocument"
        requests.post(
            url,
            json={"chat_id": chat_id, "document": document_data, "caption": caption},
        )

    def send_audio(self, chat_id, audio_data, caption=""):
        url = f"{self.base_url}/sendAudio"
        requests.post(
            url, json={"chat_id": chat_id, "audio": audio_data, "caption": caption}
        )

    def send_video(self, chat_id, video_data, caption=""):
        url = f"{self.base_url}/sendVideo"
        requests.post(
            url, json={"chat_id": chat_id, "video": video_data, "caption": caption}
        )

    def send_media_group(self, chat_id, media: list):
        if not 2 <= len(media) <= 10:
            print(f"send_media_group: need 2–10 items, got {len(media)}")
            return
        url = f"{self.base_url}/sendMediaGroup"
        requests.post(url, json={"chat_id": chat_id, "media": media})

    def handle_media_group_item(self, msg):
        chat_id = msg["chat"]["id"]
        group_id = msg["media_group_id"]

        if "photo" in msg:
            item = {
                "type": "photo",
                "media": msg["photo"][-1]["file_id"],
            }
        elif "video" in msg:
            item = {
                "type": "video",
                "media": msg["video"]["file_id"],
            }
        else:
            return

        if group_id not in self.media_groups:
            self.media_groups[group_id] = {"chat_id": chat_id, "items": []}
        self.media_groups[group_id]["items"].append(item)

    def flush_completed_groups(self, current_group_id):
        completed = [gid for gid in self.media_groups if gid != current_group_id]
        for gid in completed:
            group = self.media_groups.pop(gid)
            self.send_media_group(group["chat_id"], group["items"])

    def handle_message(self, msg):
        chat_id = msg["chat"]["id"]

        if "photo" in msg:
            file_id = msg["photo"][-1]["file_id"]
            self.send_message(chat_id, f"Here is the file_id for your photo: {file_id}")

        elif "document" in msg:
            file_name = msg["document"]["file_name"]
            file_id = msg["document"]["file_id"]
            self.send_message(
                chat_id,
                f"Here is the file_id for your '{file_name}' document: {file_id}",
            )

        elif "audio" in msg:
            title = msg["audio"]["title"]
            file_id = msg["audio"]["file_id"]
            self.send_message(
                chat_id, f"Here is the file_id for your '{title}' audio file: {file_id}"
            )

        elif "video" in msg:
            file_id = msg["video"]["file_id"]
            self.send_message(
                chat_id, f"Here is the file_id for your video file: {file_id}"
            )

        elif "text" in msg:
            text = msg["text"].strip()
            self.send_message(chat_id, f"You said: {text}")

    def start_polling(self):
        print("Bot started polling...")
        current_group_id = None

        while True:
            updates = self.get_updates()

            for result in updates:
                self.offset = result["update_id"] + 1
                msg = result.get("message")
                if not msg:
                    continue

                if "media_group_id" in msg:
                    current_group_id = msg["media_group_id"]
                    self.handle_media_group_item(msg)
                else:
                    self.flush_completed_groups(current_group_id=None)
                    current_group_id = None
                    self.handle_message(msg)

            self.flush_completed_groups(current_group_id)


if __name__ == "__main__":
    tgbot = TelegramBot(TOKEN, BASE)
    tgbot.start_polling()
