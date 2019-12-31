from app.models.product import Product
from app import db

class Coupon(db.Document):
    title = db.StringField(required=True, max_length=20)
    detail = db.StringField(required=True, max_length=40000)
    discount = db.IntField(required=True, min_value=1)
    status = db.IntField(requried=True, default=0)
    begin_time = db.DateTimeField(required=True)
    due_time = db.DateTimeField(requried=True)