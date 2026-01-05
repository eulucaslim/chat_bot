from app.core.settings import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
from pymongo import MongoClient

class MongoDBClient(object):

    def __init__(self):
        self.client = MongoClient(f"mongodb://{DATABASE_HOST}:{DATABASE_PORT}/")
        self.db = self.client[DATABASE_NAME]
    