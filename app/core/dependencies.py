from fastapi import Depends
from app.infra.gemini.provider import get_gemini_instance
from app.infra.gemini.config import Gemini
from app.services.gemini_service import GeminiService

def get_gemini_service(
		gemini: Gemini = Depends(get_gemini_instance)
) -> GeminiService:
	return GeminiService(gemini)
