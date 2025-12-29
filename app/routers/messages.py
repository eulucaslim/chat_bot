from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Dict

router = APIRouter()

@router.post("/messages", tags=['Receives Message of WebHook'])
async def receive_message(request: Request, body: Dict):
    try:
        data = request.json() if request.json() else body
        # If has content in the message
        # if data['payload']['body']:
        #     ...
        #     chatbot_session = ChatBot(data)
        #     chat_response = chatbot_session.verify_response()
        #     waha_api = WahaAPI(chatbot_session.chat_id, chat_response)
        #     # See this other day
        #     waha_api.send_seen()
            
        #     response = waha_api.send_message()
        #     db.save_answer(response)
        #     if response:
        #         return JSONResponse(
        #             content={"message": response}, 
        #             status_code=200
        #         )
        # else:
        #     raise Exception("This request no has message content!")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
