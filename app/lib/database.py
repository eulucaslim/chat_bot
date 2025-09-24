from app.config.settings import ENV, DATABASE_HOST, DATABASE_PORT
from pymongo import MongoClient

class DataBase(object):

    if ENV == "prod":
        db = MongoClient(f"mongodb://{DATABASE_HOST}:{DATABASE_PORT}/")["Messages"]
    
    def save_messages(self, data: dict) ->  None | dict[str, Exception]:
        try:
            self.db.messages.insert_one(data)
            if "_id" in data.keys():
                del data['_id']
        except Exception as e:
            return {'error': e}

    def save_answer(self, data) -> None | dict[str, Exception]:
        try:
            self.db.answer.insert_one(data)
            if "_id" in data.keys():
                del data['_id']
        except Exception as e:
            return {'error': e}