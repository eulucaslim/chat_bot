from app.lib.Gemini import Gemini
from app.lib.WahaAPI import WahaAPI
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
        return JSONResponse(content=json.loads(response), status_code=200)
    except Exception as e:
        print(e)