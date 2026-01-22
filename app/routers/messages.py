from app.core.dependencies import get_chatbot_service, get_waha_service
from app.models.message import Message, Answer
from app.services.chatbot_service import ChatBotService
from app.services.waha_service import WahaAPIService
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/messages", tags=['Receives Message of WebHook'])
async def receive_message(
    request: Request, 
    msg: Message, 
    chat_service: ChatBotService = Depends(get_chatbot_service),
    waha_service: WahaAPIService = Depends(get_waha_service)
):
    try:
        data = request.json() if request.json() else msg
        chat_response = chat_service.validate_response(data)
        # See this other day
        waha_service.send_seen()
        answer = Answer(user_id="5592991957450", ai_response=chat_response)
        response = waha_service.send_message(answer)
        if response:
            return JSONResponse(
                content={
                    "message": response
                }, 
                status_code=200
            )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
