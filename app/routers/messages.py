from app.dependencies.services import get_chatbot_service, get_evolution_service
from app.models.evolution import EvolutionWebhook
from app.services.chatbot_service import ChatBotService
from app.services.evolution_service import EvolutionService
from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/webhook/evolution", tags=['Receives Message of WebHook'], status_code=status.HTTP_200_OK)
async def receive_message(
    request: Request, 
    msg: EvolutionWebhook,
    background_tasks: BackgroundTasks,
    chat_service: ChatBotService = Depends(get_chatbot_service),
    evolution_service: EvolutionService = Depends(get_evolution_service),
):
    try:
        if request.method == "POST":
            user_number: str = msg.data.key.remoteJid
            chat_response = await chat_service.validate_response(msg, user_number)
            background_tasks.add_task(evolution_service.send, user_number, chat_response )
            return JSONResponse({"sucess": "ok"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
