from mongoengine import connect
import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = os.path.join(current_directory, '..', 'config.json')

with open(config_file_path, 'r') as f:
    config_data = json.load(f)

mongo_url = config_data.get("mongo_url")

def connect_to_mongodb():
    mongo_uri = mongo_url
    connect(host=mongo_uri)

