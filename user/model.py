from mongoengine import Document
from mongoengine import StringField

class User(Document):
    name = StringField(max_length=60, required=True, unique=True)
    email = StringField(max_length=60, required=True, unique=True)
    password = StringField(max_length=60, required=True, unique=True)
    username = StringField(max_length=60, required=True, unique=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name