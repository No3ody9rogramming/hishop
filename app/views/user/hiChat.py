from flask import redirect, render_template, url_for, flash, request, abort
from flask.views import MethodView
from flask_login import current_user

from flask_socketio import emit ##for test socketio

from app.models.user import User
from app.models.message import Message
from app import app, socketio

from mongoengine.queryset.visitor import Q

import json

class HiChatView(MethodView):
    def get(self):
        return render_template('user/hichatT.html', app=app, users=User.objects, currentUser=current_user)

    def post(self):
        senderID = request.values["senderID"]
        receiverID = request.values["receiverID"]        
        if senderID != str(current_user.id):
            abort(403)        
        messages = Message.objects((Q(sender_id=senderID) & Q(receiver_id=receiverID)) | (Q(sender_id=receiverID) & Q(receiver_id=senderID))).order_by("-create_time")
        return messages.to_json()

@socketio.on('chat message')
def handle_message(senderID, receiverID, message):
    sender = User.objects.get(id=senderID)
    data = {
        "senderID" : str(sender.id),
        "senderName": sender.name,
        "message" : message
    }
    emit(receiverID, data, broadcast=True)
    if receiverID != senderID:
        emit(senderID, data, broadcast=True)
    message = Message(sender_id=senderID, receiver_id=receiverID, message=message)
    message.save()