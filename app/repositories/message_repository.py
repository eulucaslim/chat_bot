from app.db.mongo.client import MongoClient
from app.models.message import Message, Answer
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

class MessageRepository:
	def __init__(self, db: MongoClient):
		self.messages: Collection = db["messages"]
		self.answers: Collection = db["answers"]
	
	def save_messages(self, msg: Message) ->  None | Exception:
		try:
			self.messages.insert_one(msg.model_dump())
		except (Exception, PyMongoError) as e:
			raise e

	def save_answer(self, answer: Answer) -> None | Exception:
		try:
			self.answers.insert_one(answer.model_dump())
		except (Exception, PyMongoError) as e:
			raise e