import datetime

from app.models.product import Product
from app.models.user import User
from app import db

class Order(db.Document):
    buyer_id = db.ReferenceField(User, required=True)
    product_id = db.ReferenceField(Product, required=True)
    buyer_rating = db.IntField(null=True, min_value=1, max_value=5)
    buyer_comment = db.StringField(null=True)
    seller_rating = db.IntField(null=True, min_value=1, max_value=5)
    seller_comment = db.StringField(null=True)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow())
    finish_time = db.DateTimeField(null=True)