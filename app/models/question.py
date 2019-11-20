from app.models.user import User
from app import db

class Question(db.Document):
    user_id = db.ReferenceField(User, required=True)
    title = db.StringField(required=True, max_length=20)
    detail = db.StringField(requried=True, max_length=40000)
    response = db.StringField(default=None)
    create_time = db.DateTimeField(require=True, default=datetime.datetime.utcnow())
    response_time = db.DateTimeField(default=None)
