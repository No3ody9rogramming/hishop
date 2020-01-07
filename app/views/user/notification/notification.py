from flask import request
from flask.views import MethodView
from flask_login import current_user

from app.models.message import Message

from mongoengine.queryset.visitor import Q

from app import app


class Notification(MethodView):
    def get(self):
        messages = Message.objects(
            sender_id=app.config["HISHOP_UID"],
            receiver_id=current_user.id
            ).order_by("+create_time")

        return messages.to_json()

    def post(self):
        receiverID = request.values["receiverID"]
        messages = Message.objects(
            (Q(sender_id=current_user) & Q(receiver_id=receiverID)) |
            (Q(sender_id=receiverID) & Q(receiver_id=current_user))
            ).order_by("+create_time")
        return messages.to_json()


class NotificationCount(MethodView):
    def get(self):
        print("aaaaaaaaaa")
        msgCount = Message.objects(
            (Q(sender_id__ne=app.config["HISHOP_UID"]) &
             Q(receiver_id=current_user)), isRead=False
            ).count()

        ntfCount = Message.objects(
            (Q(sender_id=app.config["HISHOP_UID"]) &
             Q(receiver_id=current_user)), isRead=False
            ).count()

        return {'msgCount': msgCount, 'ntfCount': ntfCount}

    def post(self):
        pass
