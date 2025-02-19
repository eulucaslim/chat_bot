from app.lib.Gemini import Gemini
from app.lib.WahaAPI import WahaAPI
from app.lib.DataBase import DataBase
from app.models.User import User
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json

app = FastAPI()
gemini  = Gemini()

@app.post("/receive_message")
async def receive_message(request: Request):
    try:
        response = await request.json()
        ia_response = gemini.generate_response(response["payload"]["body"])
        DataBase.save_messages(response)
        del response["_id"]
        WahaAPI.reply(
            response["payload"]["from"], 
            response["payload"]["id"], 
            ia_response
        )
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        print(e)