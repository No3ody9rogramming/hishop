from app import db

class Catogory(db.Document):
    catogory = db.StringField(required=True, Unique=True, max_length=10)