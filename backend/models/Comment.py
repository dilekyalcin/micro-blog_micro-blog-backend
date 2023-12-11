from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from Users import Users
from Post import Post 

class Comment(Document):
    content = StringField(required=True)
    author = ReferenceField(Users)
    post = ReferenceField(Post)  
    created_at = DateTimeField()
 