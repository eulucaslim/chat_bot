from app.core.settings import (
	EVOLUTION_API_URL, 
	EVOLUTION_TOKEN,
	EVOLUTION_INSTANCE
	)
from app.services.evolution_service import EvolutionService
from app.services.ai_service import AIService
from app.services.chatbot_service import ChatBotService
from fastapi import Depends

def get_ai_service() -> AIService:
	return AIService()

def get_chatbot_service(ai_service: AIService = Depends(get_ai_service)
) -> ChatBotService:
	return ChatBotService(ai_service=ai_service)


def get_evolution_service() -> EvolutionService:
	return EvolutionService(
		api_url=EVOLUTION_API_URL,
		token=EVOLUTION_TOKEN,
		instance=EVOLUTION_INSTANCE
	)
