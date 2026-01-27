from app.core.settings import WAHA_HOST, WAHA_PORT, WAHA_ADMIN
from app.models.message import Answer
import requests


class WahaAPIService:

    class WhatsError(Exception):
        pass
    
    def __init__(self):
        self.headers : dict = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        
    def send_message(self, chat_answer: Answer) -> dict | None:
        try:
            url = f"http://{WAHA_HOST}:{WAHA_PORT}/api/sendText"
            
            data = {
                "session": WAHA_ADMIN,
                "chatId": chat_answer.chat_id,
                "text": chat_answer.ai_response
            }
            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code <= 204:
                return response.json()
            else:
                raise WahaAPIService.WhatsError("Have any error in your datas, please check!")
        except Exception as e:
            raise e

    def reply(self, chat_id: int, message_id: int, text: str) -> dict:
        try:
            url = f"http://{WAHA_HOST}:{WAHA_PORT}/api/reply/"
            data = {
                "session": WAHA_ADMIN,
                "chatId": chat_id,
                "text": text,
                "reply_to": message_id
            }
            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code <= 204:
                return response.json()
            else:
                raise WahaAPIService.WhatsError("Have any error in your datas, please check!")
        except Exception as e:
            raise e
    
    def send_seen(self, chat_id: str) -> bool | Exception:
        try:
            url = f"http://{WAHA_HOST}:{WAHA_PORT}/api/sendSeen"

            data = {
                "session": WAHA_ADMIN,
                "chatId": chat_id,
            }
            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code <= 204:
                return True
            else:
                raise WahaAPIService.WhatsError("Have any error in your input, please check!")
        except Exception as e:
            raise e

