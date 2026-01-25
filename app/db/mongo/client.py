from app.core.settings import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
from pymongo import MongoClient

class MongoDBClient(object):

    def __init__(self):
        self.db = MongoClient(
            f"mongodb://{DATABASE_HOST}:{DATABASE_PORT}/")[DATABASE_NAME]
