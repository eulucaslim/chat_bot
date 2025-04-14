from app.config.settings import WAHA_HOST, WAHA_PORT, WAHA_ADMIN, WHATSAPP_HOOK_URL
from time import sleep
import requests


class WahaAPI:
    class WhatsError(Exception):
        pass
    def receive_message() -> dict:
        url = WHATSAPP_HOOK_URL
        response = requests.get(url)

        if response.status_code <= 204:
            return response.json()
        else:
            raise WahaAPI.WhatsError("Have any error in your datas, please check!")

    def send_message(chat_id: int, text: str) -> dict | None:
        url = f"http://{WAHA_HOST}:{WAHA_PORT}/api/sendText"
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "session": WAHA_ADMIN,
            "chatId": f"55{chat_id}@c.us",
            "text": text
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code <= 204:
            return response.json()
        else:
            raise WahaAPI.WhatsError("Have any error in your datas, please check!")

    def reply(chat_id: int, message_id: int, text: str):
        url = f"http://{WAHA_HOST}:{WAHA_PORT}/api/reply/"
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "session": WAHA_ADMIN,
            "chatId": f"{chat_id}",
            "text": text,
            "reply_to": message_id
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code <= 204:
            return response.json()
        else:
            raise WahaAPI.WhatsError("Have any error in your datas, please check!")
        
    def send_seen(chat_id, message_id, participant):
        url = f"http://{WAHA_HOST}:{WAHA_PORT}/api/sendSeen"
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "session": "default",
            "chatId": chat_id,
            "messageId": message_id,
            "participant": participant,
        }

        response = requests.post(url,headers=headers,json=data)
        
        if response.status_code <= 204:
            return response.json()
        else:
            raise WahaAPI.WhatsError("Have any error in your datas, please check!")