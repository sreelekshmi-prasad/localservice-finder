# providers/models.py
import mongoengine as me
from datetime import datetime

class Provider(me.Document):
    full_name = me.StringField(required=True)
    email = me.EmailField(required=True)
    phone = me.StringField()
    password = me.StringField()
    service_name = me.StringField()
    service_category = me.StringField()
    state = me.StringField()
    city = me.StringField()
    is_approved = me.BooleanField(default=False)
    created_at = me.DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'providers'}

class Service(me.Document):
    title = me.StringField(required=True)
    category = me.StringField()
    provider = me.ReferenceField(Provider)
    created_at = me.DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'services'}

class AvailabilitySlot(me.Document):
    provider = me.ReferenceField(Provider)
    service = me.ReferenceField(Service)
    date = me.DateField(required=True)
    start_time = me.StringField(required=True)
    end_time = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.utcnow)

    meta = {"collection": "availability_slots"}


class Booking(me.Document):
    slot = me.ReferenceField(AvailabilitySlot)
    customer_name = me.StringField(required=True)
    customer_email = me.StringField()
    customer_phone = me.StringField()
    booked_at = me.DateTimeField(default=datetime.utcnow)

    meta = {"collection": "bookings"}