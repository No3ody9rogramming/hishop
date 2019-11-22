import datetime

from app.models.user import User
from app.models.product import Product
from app import db, login_manager

class History(db.EmbeddedDocument):
    product_id = db.ReferenceField(Product, required=True)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow())

class Information(db.Document):
    user_id = db.ReferenceField(User, unique=True, required=True)
    history = db.ListField(db.EmbeddedDocumentField(History), default=list)
    like = db.ListField(db.ReferenceField(Product, required=True), default=list)
    cart = db.ListField(db.ReferenceField(Product, required=True), default=list)