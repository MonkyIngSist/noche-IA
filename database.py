from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]

def save_to_mongo(data, symbol):
    collection = db[config.COLLECTION_NAME]
    data['symbol'] = symbol
    collection.update_one({'symbol': symbol}, {'$set': data}, upsert=True)

def load_data():
    collection = db[config.COLLECTION_NAME]
    return list(collection.find())
