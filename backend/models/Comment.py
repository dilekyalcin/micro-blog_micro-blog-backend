from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from models.Users import Users
from models.Post import Post 


class Comment(Document):
    content = StringField(required=True)
    author = ReferenceField(Users)
    post = ReferenceField(Post)  
    created_at = DateTimeField()
 