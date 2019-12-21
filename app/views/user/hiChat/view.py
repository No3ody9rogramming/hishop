from flask import redirect, render_template, url_for, flash, request, abort
from flask.views import MethodView
from flask_login import current_user

from app.models.user import User
from app.models.message import Message

from mongoengine.queryset.visitor import Q

class HiChatView(MethodView):
    def get(self):
        messagesList = []
        messagesOwners = Message.objects(sender_id=current_user.id).order_by("+create_time")
        for m in messagesOwners:
            messagesList.append(m)
        messagesOwners = Message.objects(receiver_id=current_user.id).order_by("+create_time")
        for m in messagesOwners:
            m.receiver_id = m.sender_id
            messagesList.append(m)
        messagesList = sorted(messagesList, key = lambda i: i.create_time)
        users = {}
        for m in messagesList:
        	users[str(m.receiver_id.id)] = m #user dictionary to prevent duplicate
        users = sorted(users.items(), key = lambda i: i[1].create_time, reverse=True)
        return render_template('user/hichatT.html', Tusers=User.objects, users=users, currentUser=current_user)

    def post(self):
        receiverID = request.values["receiverID"]
        messages = Message.objects((Q(sender_id=current_user) & Q(receiver_id=receiverID)) | (Q(sender_id=receiverID) & Q(receiver_id=current_user))).order_by("+create_time")
        return messages.to_json()