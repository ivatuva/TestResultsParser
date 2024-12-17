from .mongodb_client import MongoDBClient
from typing import Any


class DAO:
    def __init__(self, mongodb_client: MongoDBClient):
        self.mongodb_client = mongodb_client
        self.collection_name = "results"

    def save(self, data: Any):
        collection = self.mongodb_client.get_collection(self.collection_name)
        collection.insert_one(data)