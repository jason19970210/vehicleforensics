from pymongo import MongoClient


client = MongoClient()

client = MongoClient('localhost', 27017)

db = client['vehicle']


print(db)
