from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from models.Users import Users
from models.Tag import Tags


class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(Users)  
    created_at = DateTimeField()
    tag = ReferenceField(Tags)
    # image_filename = StringField()