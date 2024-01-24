from mongoengine import Document, ReferenceField
from models.Users import Users
from models.Post import Post

class Like(Document):
    user = ReferenceField(Users)
    post = ReferenceField(Post)
