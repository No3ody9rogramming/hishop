from app import db

class Keyword(db.Document):
    keyword = db.StringField(required=True, Unique=True)
    count = db.IntField(required=True, default=0)