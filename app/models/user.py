from flask_login import UserMixin
import datetime

from app import db, login_manager

class User(UserMixin, db.Document):
    name = db.StringField(required=True, max_length=50)
    account = db.StringField(required=True, unique=True, min_length=4, max_length=20)
    password = db.StringField(required=True)
    born = db.DateTimeField(required=True)
    phone = db.StringField(required=True, max_length=15)
    hicoin = db.LongField(required=True, default=0)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow())
    
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()