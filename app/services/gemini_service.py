from app.infra.entities.gemini import Gemini
from app.models.message import Message, Answer
from app.repositories.message_repository import MessageRepository
from pathlib import Path

class GeminiService(object):
	def __init__(self, gemini: Gemini, message_repository: MessageRepository):
		self.gemini = gemini
		self.message_repository = message_repository

	def generate_response(self, msg: Message, path: Path) -> str | None:
		self.message_repository.save_messages(msg)
		prompt = self.read_prompt(path)
		ai_response = self.gemini.generate_response(prompt + msg.content)
		answer = Answer(user_id=msg.user_number, ai_response=ai_response)
		self.message_repository.save_answer(answer)
		return ai_response

	def read_prompt(self, path: Path) -> str:
		with open(path, "r", encoding='utf-8') as prompt:
			return prompt.read()
