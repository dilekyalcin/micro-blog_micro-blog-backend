from mongoengine import connect
import os

def connect_to_mongodb():
    mongo_uri = os.environ.get("MONGO_URL")
    connect(host=mongo_uri)

# connect MongoDb
connect_to_mongodb()
