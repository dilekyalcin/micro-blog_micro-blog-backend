from mongoengine import connect
import pymongo

def connect_to_database(uri, _cls=pymongo.MongoClient):
    connect(host=uri, alias='default', mongo_client_class=_cls)
    return True