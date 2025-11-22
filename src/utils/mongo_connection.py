from pymongo import MongoClient

class MongoConnection:
    def __init__(self):
        mongo_uri = "mongodb://mongoadmin:secret@localhost:27017/"
        self.client = MongoClient(mongo_uri)
        self.db = self.client["labdatabase"] 

    def get_db(self):
        return self.db
