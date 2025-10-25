from django.db import models

# Create your models here.
# adminpanel/models.py
from datetime import datetime
import mongoengine as me
from werkzeug.security import generate_password_hash, check_password_hash
from providers.models import Provider

class AdminUser(me.Document):
    email = me.EmailField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    name = me.StringField(max_length=100)
    meta = {'collection': 'admin_users'}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(me.Document):
    name = me.StringField(required=True, unique=True)
    description = me.StringField()
    created_at = me.DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'categories'}


class Provider(me.Document):
    name = me.StringField(required=True)
    email = me.EmailField(required=True)
    phone = me.StringField()
    address = me.StringField()
    created_at = me.DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'providers'}


class Customer(me.Document):
    name = me.StringField(required=True)
    email = me.EmailField(required=True)
    phone = me.StringField()
    created_at = me.DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'customers'}


class Service(me.Document):
    title = me.StringField(required=True)
    description = me.StringField()
    category = me.ReferenceField(Category)
    provider = me.ReferenceField(Provider)
    price = me.FloatField(default=0)
    created_at = me.DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'services'}


class Review(me.Document):
    service = me.ReferenceField(Service)
    customer = me.ReferenceField(Customer)
    rating = me.IntField(min_value=1, max_value=5)
    comment = me.StringField()
    created_at = me.DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'reviews'}
