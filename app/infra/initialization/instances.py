from app.infra.entities.gemini import Gemini
from app.db.mongo.client import MongoDBClient

_gemini_instance : Gemini | None = None
_db_instance: MongoDBClient | None = None


class Instance(object):

	def get_gemini_instance() -> Gemini:
		global _gemini_instance

		if _gemini_instance is None:
			_gemini_instance = Gemini()
		return _gemini_instance
	
	def get_db_instance() -> MongoDBClient:
		global _db_instance

		if _db_instance is None:
			_db_instance = MongoDBClient()
		return _db_instance

