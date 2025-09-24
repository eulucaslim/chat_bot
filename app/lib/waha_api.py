from app.config.settings import WAHA_HOST, WAHA_PORT, WAHA_ADMIN, WHATSAPP_HOOK_URL
import requests


class WahaAPI:

    class WhatsError(Exception):
        pass
    
    def __init__(self, chat_id: int, chat_response):
        self.chat_id = chat_id
        self.ai_response = chat_response
        
    def send_message(self) -> dict | None:
        try:
            url = f"http://{WAHA_HOST}:{WAHA_PORT}/api/sendText"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            data = {
                "session": WAHA_ADMIN,
                "chatId": self.chat_id,
                "text": self.ai_response
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code <= 204:
                return response.json()
            else:
                raise WahaAPI.WhatsError("Have any error in your datas, please check!")
        except Exception as e:
            return {"message": e}

    def reply(self, chat_id: int, message_id: int, text: str) -> dict:
        try:
            url = f"http://{WAHA_HOST}:{WAHA_PORT}/api/reply/"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            data = {
                "session": WAHA_ADMIN,
                "chatId": chat_id,
                "text": text,
                "reply_to": message_id
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code <= 204:
                return response.json()
            else:
                raise WahaAPI.WhatsError("Have any error in your datas, please check!")
        except Exception as e:
            return {"message": e}
    
    def send_seen(self) -> dict | Exception:
        try:
            url = f"http://{WAHA_HOST}:{WAHA_PORT}/api/sendSeen"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            data = {
                "session": WAHA_ADMIN,
                "chatId": self.chat_id,
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code <= 204:
                return response.json()
            else:
                raise WahaAPI.WhatsError("Have any error in your datas, please check!")
        except Exception as e:
            return {"message": e}

