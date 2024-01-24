from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from models.Users import Users  


class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(Users)  
    created_at = DateTimeField()
    # image_filename = StringField()

