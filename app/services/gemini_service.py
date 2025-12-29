from app.infra.gemini.config import Gemini

class GeminiService(object):
	def __init__(self, gemini: Gemini):
			self.gemini = gemini
													
	def welcome(self, msg: str) -> str | None:
			welcome_words = self.read_prompt(self.gemini.welcome_path)
			return self.gemini.generate_response(welcome_words + msg)
	
	def default_answer(self, msg: str) -> str | None:
			default_prompt = self.read_prompt(self.gemini.default_path)
			return self.gemini.generate_response(default_prompt + msg) 

	def insert_data(self, msg: str) -> str | None:
			insert_prompt = self.read_prompt(self.gemini.insert_path)
			return self.gemini.generate_response(insert_prompt + msg)

	def read_prompt(self, path: str) -> str:
			with open(path, "r", encoding='utf-8') as prompt:
					return prompt.read()