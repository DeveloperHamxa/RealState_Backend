# from enum import unique
# from mongoengine import Document
# from mongoengine import StringField, IntField

# class User(Document):
#     name = StringField(max_length=60, required=True, unique=True)
#     email = StringField(max_length=60, required=True, unique=True)
#     password = StringField(max_length=60, required=True, unique=True)
#     username = StringField(max_length=60, required=True, unique=True)

#     def __unicode__(self):
#         return self.name

#     def __repr__(self):
#         return self.name


# class Estate(Document):
#     id=IntField(primary_key=True, unique=True)
#     name = StringField(max_length=60, required=True, unique=True)
#     description = StringField(max_length=60, required=True, unique=True)
#     city = StringField(max_length=60, required=True, unique=True)
#     room = StringField(max_length=60, required=True, unique=True)
    