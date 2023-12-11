from mongoengine import connect

def connect_to_mongodb():
    mongo_uri = "mongodb+srv://Dilek:Dilek1405.@cluster0.chl5nrw.mongodb.net/micro-blogDB?retryWrites=true&w=majority"
    connect(host=mongo_uri)

