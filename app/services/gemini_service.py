from app.infra.entities.gemini import Gemini
from app.models.message import Message, Answer
from app.repositories.message_repository import MessageRepository

class GeminiService(object):
	def __init__(self, gemini: Gemini, message_repository: MessageRepository):
		self.gemini = gemini
		self.message_repository = message_repository
													
	def welcome(self, msg: Message) -> str | None:
		self.message_repository.save_messages(msg)
		welcome_words = self.read_prompt(self.gemini.welcome_path)
		ai_response = self.gemini.generate_response(welcome_words + msg.content)
		answer = Answer(msg.user_number, ai_response)
		self.message_repository.save_answer(answer)
		return ai_response
	
	def default_answer(self, msg: Message) -> str | None:
		self.message_repository.save_messages(msg)
		default_prompt = self.read_prompt(self.gemini.default_path)
		ai_response = self.gemini.generate_response(default_prompt + msg.content) 
		answer = Answer(msg.user_number, ai_response)
		self.message_repository.save_answer(answer)
		return ai_response
	
	def insert_data(self, msg: Message) -> str | None:
		self.message_repository.save_messages(msg)
		insert_prompt = self.read_prompt(self.gemini.insert_path)
		ai_response = self.gemini.generate_response(insert_prompt + msg.content)
		answer = Answer(msg.user_number, ai_response)
		self.message_repository.save_answer(answer)
		return ai_response

	def read_prompt(self, path: str) -> str:
		with open(path, "r", encoding='utf-8') as prompt:
			return prompt.read()