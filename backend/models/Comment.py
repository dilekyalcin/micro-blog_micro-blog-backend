from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from models.users import Users
from models.post import Post 

class Comment(Document):
    content = StringField(required=True)
    author = ReferenceField(Users)
    post = ReferenceField(Post)  
    created_at = DateTimeField()
 