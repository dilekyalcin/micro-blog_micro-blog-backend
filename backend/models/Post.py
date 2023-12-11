from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from Users import Users  

class Post(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    author = ReferenceField(Users)  
    created_at = DateTimeField()
    likes = ListField(ReferenceField(Users))  
    comments = ListField(ReferenceField('Comment'))
