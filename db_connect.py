
import pymongo
from dotenv import dotenv_values

config = dotenv_values(".env")

password = config["PASSWORD"]

path = "mongodb+srv://enterindarkness:" + password + "@cluster1.f2h8nvo.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(path)
db = client.semantic_search
