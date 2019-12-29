from app import db

class Category(db.Document):
    category = db.StringField(required=True, Unique=True, max_length=10)