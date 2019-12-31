import datetime

from app.models.product import Product
from app.models.user import User
from app import db

#移交中 領收中 已完成 已取消 全部
ORDER_STATUS = {"TRANSFERING" : "0", "RECEIPTING" : "1", "COMPLETE" : "2", "CANCEL" : "3", "ALL" : "4"}

class Order(db.Document):
    buyer_id = db.ReferenceField(User, required=True)
    product_id = db.ReferenceField(Product, required=True)
    buyer_rating = db.IntField(null=True, min_value=1, max_value=5)
    buyer_comment = db.StringField(null=True)
    seller_rating = db.IntField(null=True, min_value=1, max_value=5)
    seller_comment = db.StringField(null=True)
    status = db.IntField(required=True, default=0, min_value=0, max_value=3)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow()+datetime.timedelta(hours=8))
    transfer_time = db.DateTimeField(null=True)
    finish_time = db.DateTimeField(null=True)