import mongoengine as me

class Customer(me.Document):
    name = me.StringField(required=True)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)
    phone = me.StringField()

    meta = {"collection": "customers"}

    def __str__(self):
        return self.name
