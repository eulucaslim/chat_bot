from app.dependencies.repositories import RepositoryImp
from app.infra.initialization.instances import Instance
from app.infra.entities.gemini import Gemini
from app.services.evolution_service import EvolutionService
from app.services.gemini_service import GeminiService
from app.services.chatbot_service import ChatBotService
from app.repositories.message_repository import MessageRepository
from fastapi import Depends

def get_gemini_service(
	gemini: Gemini = Depends(Instance.get_gemini_instance),
	message_repository: MessageRepository = Depends(RepositoryImp.get_message_repository)
) -> GeminiService:
	return GeminiService(gemini, message_repository)

def get_chatbot_service(gemini_service: GeminiService = Depends(get_gemini_service)
) -> ChatBotService:
	return ChatBotService(gemini_service=gemini_service)


def get_evolution_service() -> EvolutionService:
	return EvolutionService(EVOLUTION_TOKEN=429683C4C977415CAAFCCE10F7D57E11
EVOLUTION_API_URL="https://singu-evolution.marcusbrandt.dev"
WEBHOOK_URL_EVOLUTION="https://mt56vl37ehbb.shares.zrok.io/webhook/evolution")
