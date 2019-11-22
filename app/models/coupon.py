from app.models.product import Product
from app import db

class Catogory(db.Document):
    title = db.StringField(required=True, max_length=20)
    detail = db.StringField(required=True, max_length=40000)
    discount = db.FloadField(required=True)
    create_time = db.DateTimeField(required=True)
    due_time = db.DateTimeField(requried=True)