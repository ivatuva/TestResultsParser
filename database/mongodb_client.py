import yaml
from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        mongodb_config = config['mongodb']
        uri = mongodb_config['uri']
        database_name = mongodb_config['database_name']
        
        self.client = MongoClient(uri)
        self.database = self.client[database_name]

    def get_collection(self, collection_name: str):
        return self.database[collection_name]
