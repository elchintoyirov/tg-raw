import requests

from config import BASE, TOKEN

offset = 0


class TelegramBot:
    def __init__(self, token, base_url):
        self.token = token
        self.base_url = f"{base_url}{token}"
        self.offset = 0

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
        payload = {"chat_id": chat_id, "text": text}
        requests.post(url, json=payload)

    def send_photo(self, chat_id, photo_data, caption=""):
        url = f"{self.base_url}/sendPhoto"
        payload = {"chat_id": chat_id, "photo": photo_data, "caption": caption}
        requests.post(url, json=payload)

    def send_document(self, chat_id, document_data, caption=""):
        url = f"{self.base_url}/sendDocument"
        payload = {"chat_id": chat_id, "document": document_data, "caption": caption}
        requests.post(url, json=payload)

    def send_audio(self, chat_id, audio_data, caption=""):
        url = f"{self.base_url}/sendAudio"
        payload = {"chat_id": chat_id, "audio": audio_data, "caption": caption}
        requests.post(url, json=payload)

    def send_video(self, chat_id, video_data, caption=""):
        url = f"{self.base_url}/sendVideo"
        payload = {"chat_id": chat_id, "video": video_data, "caption": caption}
        requests.post(url, json=payload)

    def identify_file_type(self, file_id):
        url = f"{self.base_url}/getFile"
        try:
            response = requests.get(url, params={"file_id": file_id}).json()

            file_path = response["result"].get("file_path", "")

            if file_path.startswith("photos/"):
                return "photo"
            elif file_path.startswith("document/"):
                return "document"
            elif file_path.startswith("videos/"):
                return "videos"
            elif file_path.startswith("music/") or file_path.startswith("audio/"):
                return "audio"
            return "document"

        except Exception:
            return "regular_text"

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
            file_type = self.identify_file_type(text)

            if file_type == "photo":
                self.send_photo(chat_id, text, caption="Sent via Cloud")
            elif file_type == "document":
                self.send_document(chat_id, text, caption="Sent via Cloud")
            elif file_type == "audio":
                self.send_audio(chat_id, text, caption="Sent via Cloud")
            elif file_type == "videos":
                self.send_video(chat_id, text, caption="Sent via Cloud")

    def start_polling(self):
        print("Bot started polling...")

        while True:
            updates = self.get_updates()

            for result in updates:
                self.offset = result["update_id"] + 1

                msg = result.get("message")
                if msg:
                    self.handle_message(msg)


if __name__ == "__main__":
    tgbot = TelegramBot(TOKEN, BASE)
    tgbot.start_polling()
