from app.db.mongo.client import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from typing import Dict

class MessageRepository:
	def __init__(self, db: MongoClient):
			self.messages: Collection = db["messages"]
			self.answers: Collection = db["answers"]
	
	def save_messages(self, data: Dict) ->  None | Exception:
		try:
			self.messages.insert_one(data)
		except (Exception, PyMongoError) as e:
				raise e

	def save_answer(self, data: Dict) -> None | Exception:
			try:
				self.answers.insert_one(data)
			except (Exception, PyMongoError) as e:
				raise e