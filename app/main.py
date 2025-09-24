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
async def receive_message(request: Request):
    try:
        data = await request.json()
        # If has content in the message
        if data['payload']['body']:
            db.save_messages(data)
            chatbot_session = ChatBot(data)
            chat_response = chatbot_session.verify_response()
            waha_api = WahaAPI(chatbot_session.chat_id, chat_response)
            # See this other day
            waha_api.send_seen()
            
            response = waha_api.send_message()
            db.save_answer(response)
            if response:
                return JSONResponse(
                    content={"message": response}, 
                    status_code=200
                )
        else:
            raise Exception("This request no has message content!")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
