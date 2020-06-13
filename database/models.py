from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class Event(db.Document):
    title = db.StringField(required=True)
    description = db.StringField()
    start = db.DateTimeField(required=True)
    end = db.DateTimeField(required=True)
    owner = db.ReferenceField("User")


class User(db.Document):
    email = db.StringField(required=True, unique=True)
    first_name = db.StringField(max_length=50, required=True)
    last_name = db.StringField(max_length=50, required=True)
    password = db.StringField(min_length=8, required=True)
    events = db.ListField(db.ReferenceField("Event", reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)

User.register_delete_rule(Event, "owner", db.CASCADE)
