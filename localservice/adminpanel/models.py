# adminpanel/models.py
from datetime import datetime
import mongoengine as me
from werkzeug.security import generate_password_hash, check_password_hash
from providers.models import Provider, Service
from customers.models import Customer


# DO NOT import Provider or Service here
# They belong to the providers app

class AdminUser(me.Document):
    email = me.EmailField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    name = me.StringField(max_length=100)
    meta = {'collection': 'admin_users'}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Review(me.Document):
    service = me.ReferenceField("Service")     # Use string reference
    customer = me.ReferenceField(Customer)
    rating = me.IntField(min_value=1, max_value=5)
    comment = me.StringField()
    created_at = me.DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'reviews'}
