from django.db import models

# Create your models here.
from mongoengine import Document, StringField

class Customer(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    phone = StringField()
