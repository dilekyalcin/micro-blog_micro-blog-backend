from mongoengine import Document, StringField, EmailField, DateTimeField, ListField, ReferenceField
import datetime


class Users(Document):
    firstname = StringField()
    lastname = StringField()
    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    password_salt = StringField(required=True) 
    email = EmailField(required=True, unique=True)
    bio = StringField(max_length=800)
    birthdate = DateTimeField()
    created_at = DateTimeField(default=datetime.datetime.now)
