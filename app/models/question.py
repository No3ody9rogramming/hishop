import datetime

from app.models.user import User
from app import db

class Question(db.Document):
    user_id = db.ReferenceField(User, required=True)
    title = db.StringField(required=True, max_length=20)
    detail = db.StringField(requried=True, max_length=4000)
    response = db.StringField(null=True, max_length=4000)
    create_time = db.DateTimeField(require=True, default=datetime.datetime.utcnow()+datetime.timedelta(hours=8))
    response_time = db.DateTimeField(null=True)
