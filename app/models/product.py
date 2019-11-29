import datetime

from app.models.catogory import Catogory
from app.models.user import User
from app import db

class Bid(db.EmbeddedDocument):
    per_price = db.IntField(required=True, min_value=1, max_value=1000)
    low_price = db.IntField(requried=True, min_value=1, max_value=10000)
    now_price = db.IntField(requried=True, min_value=0, max_value=100000, default=0)
    buyer_id = db.ReferenceField(User, null=True)
    due_time = db.DateTimeField(required=True)

class Product(db.Document):
    seller_id = db.ReferenceField(User, required=True)
    name = db.StringField(required=True, max_length=20)
    price = db.IntField(required=True, min_value=1, max_value=100000)
    bid = db.EmbeddedDocumentField(Bid, null=True)
    discount = db.FloatField(required=True, min_value=0., max_value=1., default=1.)
    detail = db.StringField(required=True, max_length=40000)
    image = db.StringField(required=True)
    view = db.IntField(required=True, default=0)
    categories = db.ListField(db.ReferenceField(Catogory), default=list)
    bidding = db.BooleanField(requried=True)
    status = db.IntField(requried=True, default=0)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow())