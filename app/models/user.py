from flask import abort
from flask_login import UserMixin, current_user, logout_user
import datetime

from app import db, login_manager

class User(UserMixin, db.Document):
    account = db.StringField(required=True, unique=True, min_length=4, max_length=20)
    password = db.StringField(required=True)
    name = db.StringField(required=True, min_length=2, max_length=20)
    store_name = db.StringField(required=True, min_length=2, max_length=20)
    icon = db.StringField(required=True, default="default.png")
    email = db.StringField(required=True, unique=True)
    phone = db.StringField(required=True, max_length=15)
    birth = db.DateTimeField(required=True)
    address = db.StringField(required=True, max_length=50)
    prefer_begin_time = db.StringField(required=True, max_length=10)
    prefer_end_time = db.StringField(requried=True, max_length=10)
    status = db.IntField(required=True, default=0)
    hicoin = db.LongField(required=True, min_value=0, default=0)
    reset_token = db.StringField(null=True)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow()+datetime.timedelta(hours=8))
    
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

def check_admin(func):
    def wrap(*args, **kwargs):
        if current_user.status != 2:
            return abort(403)
        else:
            return func(*args, **kwargs)
    return wrap

def check_activate(func):
    def wrap(*args, **kwargs):
        if current_user.status not in [1, 2]:
            logout_user()
            return abort(403)
        else:
            return func(*args, **kwargs)
    return wrap