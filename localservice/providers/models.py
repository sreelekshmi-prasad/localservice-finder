# providers/models.py
from mongoengine import Document, StringField, EmailField, ReferenceField, DateTimeField
from datetime import datetime

class Provider(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    phone = StringField()
    bio = StringField()
    state = StringField()
    city = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.full_name  # helps when displaying in admin templates


class Service(Document):
    provider = ReferenceField(Provider, required=True, reverse_delete_rule=2)  # CASCADE
    title = StringField(required=True)
    category = StringField()  # simple string category (not a separate Category model)
    description = StringField()  # add this to show description
    created_at = DateTimeField(default=datetime.utcnow)
