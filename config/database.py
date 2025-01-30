from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_DB_CONNECTION_STRING"))

db = client[os.getenv("DATABASE_NAME")]

user_collection = db['user']
nn_collection = db['neural_network']