from mongoengine import Document, StringField

class Token(Document):
    jti = StringField(unique=True, required=True)