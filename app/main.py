from app.lib.chatbot import ChatBot
from app.lib.waha_api import WahaAPI
from app.lib.database import DataBase
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import json

app = FastAPI(
    title="ChatBot in Python!",
    version="1.0.0"
)

db = DataBase()


@app.post("/receive_message", tags=['Webhook'])
async def receive_message(request: Request) -> dict:
    try:
        data = await request.json()
        # If has content in the message
        if data['payload']['body']:
            db.save_messages(data)
            chatbot_session = ChatBot(data)
            ai_response = chatbot_session.verify_response()
            waha_api = WahaAPI(chatbot_session.chat_id, ai_response)
            # See this other day
            response = waha_api.send_seen()
            if response:
                return JSONResponse(
                    content={"message": response}, 
                    status_code=200
                )
            else:
                return JSONResponse(
                    content={"message": response}, 
                    status_code=400
                )
        else:
            raise Exception("This request no has message content!")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
