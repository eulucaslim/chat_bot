from app.lib.gemini import Gemini
from app.lib.waha_api import WahaAPI
from app.lib.database import DataBase
from app.utils.prompts import welcome_words
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()
gemini  = Gemini()
db = DataBase()

@app.post("/receive_message")
async def receive_message(request: Request):
    try:
        response = await request.json()
        ia_response = gemini.generate_response(welcome_words() + response["payload"]["body"])
        db.save_answer(ia_response)
        db.save_messages(response)
        del response["_id"]
        WahaAPI.reply(
            response["payload"]["from"], 
            response["payload"]["id"], 
            ia_response
        )
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)