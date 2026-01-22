from app.infra.initialization.instances import Instance
from app.infra.entities.gemini import Gemini
from app.services.gemini_service import GeminiService
from app.services.chatbot_service import ChatBotService
from app.services.waha_service import WahaAPIService
from app.repositories.message_repository import MessageRepository
from fastapi import Depends

def get_gemini_service(
	gemini: Gemini = Depends(Instance.get_gemini_instance),
	message_repository: MessageRepository = Depends(Instance.get_repository_instance)
) -> GeminiService:
	return GeminiService(gemini, message_repository)

def get_chatbot_service(gemini_service: GeminiService = Depends(get_gemini_service)
) -> ChatBotService:
	return ChatBotService(gemini_service=gemini_service)

def get_waha_service() -> WahaAPIService:
	return WahaAPIService()