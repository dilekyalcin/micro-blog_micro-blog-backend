from mongoengine import Document, StringField, IntField

class Tags(Document):
    tag_name = StringField()
    count = IntField(default=0)