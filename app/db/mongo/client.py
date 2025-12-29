from app.core.settings import ENV, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
from pymongo import MongoClient
from typing import Dict

class MongoDBClient(object):

    def __init__(self):
        self.client = MongoClient(f"mongodb://{DATABASE_HOST}:{DATABASE_PORT}/")
        self.db = self.client[DATABASE_NAME]
    