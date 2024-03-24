from mongoengine import Document, StringField, IntField

class Tags(Document):
    tag_name = StringField()
    popularity_score = IntField(default=0)