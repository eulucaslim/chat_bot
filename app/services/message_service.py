from app.lib.waha_api import WahaAPI
from app.lib.database import DataBase
from app.lib.sheets import Sheets

class MessageService:
    def __init__(self):
        self.sheets = Sheets()
        self.db = DataBase()
        self.waha_api = WahaAPI()

    async def process_message(self, response: dict) -> None:
        ia_response = self.sheets.verify_response(response["payload"]["body"])

        self.db.save_answer(ia_response)
        self.db.save_messages(response)

        self.waha_api.reply(
            response["payload"]["from"], 
            response["payload"]["id"], 
            ia_response
        )