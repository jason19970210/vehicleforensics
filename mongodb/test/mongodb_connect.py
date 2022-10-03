import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_IP = os.getenv("MONGODB_IP")
MONGODB_PORT = int(os.getenv("MONGODB_PORT"))
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")

client = MongoClient()

client = MongoClient(f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_IP}:{MONGODB_PORT}/?authMechanism=DEFAULT&authSource={MONGODB_DBNAME}")

db = client[MONGODB_DBNAME]

for collection in db.list_collection_names():
    print(collection)
