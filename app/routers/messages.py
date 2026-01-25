from app.dependencies.services import get_chatbot_service, get_waha_service
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
        if request.method == "POST":
            chat_response = chat_service.validate_response(msg)
            # See this other day
            waha_service.send_seen()
            answer = Answer(
                user_id=msg.user_number,
                ai_response=chat_response
            )
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
