from flask_login import UserMixin
import datetime

from app import db, login_manager

class Address(db.EmbeddedDocument):
    address = db.StringField(required=True, max_length=50)
    begin = db.StringField(required=True, max_length=10)
    end = db.StringField(requried=True, max_length=10)

class User(UserMixin, db.Document):
    account = db.StringField(required=True, unique=True, min_length=4, max_length=20)
    password = db.StringField(required=True)
    name = db.StringField(required=True, min_length=2, max_length=20)
    store_name = db.StringField(required=True, min_length=2, max_length=20)
    icon = db.StringField(required=True, default="default.png")
    email = db.StringField(required=True, unique=True)
    phone = db.StringField(required=True, max_length=15)
    birth = db.DateTimeField(required=True)
    address = db.ListField(db.EmbeddedDocumentField(Address), default=list)
    status = db.IntField(required=True, default=0)
    hicoin = db.LongField(required=True, min_value=0, default=0)
    reset_token = db.StringField(null=True)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow())
    
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()