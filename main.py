from app.lib.Gemini import Gemini
from app.lib.WahaAPI import WahaAPI
from app.models.User import User
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
waha = WahaAPI()
gemini  = Gemini()

@app.post("/send_message")
def send_message_whatsapp(user: User):
    try:
        response = waha.send_message(user.phone_number, user.text)
        return JSONResponse(content={"msg": str(response)}, status_code=200)
    except Exception as e:
        print(e)