from app.infra.entities.gemini import Gemini
from app.repositories.message_repository import MessageRepository
from app.db.mongo.client import MongoDBClient

_gemini_instance : Gemini | None = None
_repository_instance: MessageRepository | None = None
_db_instance: MongoDBClient | None = None


class Instance(object):

	def get_gemini_instance() -> Gemini:
		global _gemini_instance

		if _gemini_instance is None:
			_gemini_instance = Gemini()
		return _gemini_instance
	
	def get_repository_instance() -> MessageRepository:
		global _repository_instance

		if _repository_instance is None:
			_repository_instance = MessageRepository()
		return _repository_instance

