from app.config.settings import ENV, DATABASE_HOST, DATABASE_PORT
from pymongo import MongoClient

class DataBase(object):

    if ENV == "prod":
        db: MongoClient = MongoClient(
            f"mongodb://{DATABASE_HOST}:{DATABASE_PORT}/"
            f"?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.8")["Messages"]
    
    def save_messages(self, data: dict) -> None:
        try:
            self.db.messages.insert_one(data)
            if "_id" in data.keys():
                del data['_id']
        except Exception as e:
            return {'error': e}

    def save_answer(self, data: str) -> None:
        try:
            self.db.answer.insert_one({"answer": data})
        except Exception as e:
            return {'error': e}