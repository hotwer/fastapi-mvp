from pymongo import MongoClient
from globals import *

def db():
    client = MongoClient(MONGO_CONNECTION_STRING)
    return client[MONGO_DATABASE_NAME]
