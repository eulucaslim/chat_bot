from config.settings import ENV, DATABASE_HOST, DATABASE_PORT
from pymongo import MongoClient

class DataBase(object):

    if ENV == "prod":
        db: MongoClient = MongoClient(
            f"mongodb://{DATABASE_HOST}:{DATABASE_PORT}/"
            f"?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.8")["Messages"]
    
    def save_messages(self, data: dict) -> None:
        try:
            self.db.messages.insert_one(data)
        except Exception as e:
            print(e)