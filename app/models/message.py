import datetime

from app.models.user import User
from app import db

class Message(db.Document):
    sender_id = db.ReferenceField(User, required=True)
    receiver_id = db.ReferenceField(User, required=True)
    message = db.StringField(required=True)
    create_time = db.DateTimeField(require=True, default=datetime.datetime.utcnow())
