import datetime

from app import db

class Product(db.Document):
    seller_id = db.ObjectIdField()
    buyer_id = db.ObjectIdField()
    name = db.StringField(required=True, max_length=50)
    price = db.IntField(required=True, min_value=1, max_value=100000)
    step = db.IntField(required=True, default=None, min_value=1, max_value=1000)
    detail = db.StringField(required=True, max_length=40000)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow())