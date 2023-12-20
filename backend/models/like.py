from mongoengine import Document, ReferenceField
from models.users import Users
from models.post import Post

class Like(Document):
    user = ReferenceField(Users)
    post = ReferenceField(Post)
