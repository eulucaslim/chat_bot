from app.db.mongo.client import MongoDBClient

class DatabaseImp:

	@staticmethod
	def get_database() -> MongoDBClient:
		return MongoDBClient()
