from pymongo import MongoClient


class MongodbConnect:
    def __init__(self, host: str, port: int, username: str, password: str, dbname: str, col: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname
        self.col = None

        self.client = MongoClient(f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/?authSource={self.dbname}")
        self.db = self.client[self.dbname]

    def set_collection(self, col: str):
        """ Set the collection to be used for MongoDB operations """
        self.collection = self.db[col]

    def insert_mongodb(self, data):
        result = self.collection.insert_one(data)
        print(f"Inserted record ID: {result.inserted_id}")

    def __del__(self):
        self.client.close()