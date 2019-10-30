import datetime

from app import db

class Payment(db.Document):
    payer_id = db.ObjectIdField(required=True)
    transaction_id = db.LongField(required=True, unique=True)
    amount = db.IntField(required=True, min_value=1, max_value=100000)
    currency = db.StringField(required=True)
    confirm = db.BooleanField(required=True)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow())