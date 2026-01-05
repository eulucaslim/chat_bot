from app.infra.gemini.config import Gemini

_gemini_instance = Gemini = None

def get_gemini_instance() -> Gemini:
	global _gemini_instance

	if _gemini_instance is None:
		_gemini_instance = Gemini()
	return _gemini_instance

