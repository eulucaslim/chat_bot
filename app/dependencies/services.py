from app.core.settings import (
	EVOLUTION_API_URL, 
	EVOLUTION_TOKEN,
	EVOLUTION_INSTANCE
	)
from app.services.evolution_service import EvolutionService
from app.services.ai_service import AIService
from app.services.chatbot_service import ChatBotService
from app.dependencies.redis import RedisConnection
from fastapi import Depends

def get_ai_service() -> AIService:
	return AIService()

def get_redis_service() -> RedisConnection:
	return RedisConnection()

def get_chatbot_service(
		ai_service: AIService = Depends(get_ai_service), 
		redis_service: RedisConnection = Depends(get_redis_service)
) -> ChatBotService:
	return ChatBotService(ai_service=ai_service, redis=redis_service)


def get_evolution_service() -> EvolutionService:
	return EvolutionService(
		api_url=EVOLUTION_API_URL,
		token=EVOLUTION_TOKEN,
		instance=EVOLUTION_INSTANCE
	)
