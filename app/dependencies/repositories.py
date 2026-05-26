from app.db.mongo.client import MongoDBClient
from app.dependencies.db import DatabaseImp
from app.repositories.message_repository import MessageRepository
from fastapi import Depends


class RepositoryImp:

	@staticmethod
	def get_message_repository(
			db: MongoDBClient = Depends(DatabaseImp.get_database)
	) -> MessageRepository:
		return MessageRepository(db)
